"""
Three-Question Study Machine - Backend Middleware

FastAPI server that serves as middleware between the HarmonyOS frontend
and the DeepSeek AI API. Provides SSE streaming for real-time AI evaluation.
"""

import json
import logging
import os
import time

from dotenv import load_dotenv

# Load environment variables FIRST before importing deepseek_client
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from services.deepseek_client import deepseek_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Three-Question Study Machine API",
    description="Backend middleware for AI-powered learning evaluation",
    version="1.0.0",
)

# CORS middleware (allow all for MVP)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class EvaluateRequest(BaseModel):
    """Request model for AI evaluation endpoint."""
    step_type: str = Field(..., description="Learning step: 'what', 'why', 'how', or 'review'")
    knowledge_point_title: str = Field(..., description="Title of the knowledge point")
    user_input: str = Field(..., min_length=20, description="Student's answer text")
    knowledge_point_content: str = Field(default="", description="Reference content for evaluation")
    follow_up_context: str = Field(default="", description="Previous conversation context for follow-up evaluation")
    review_mode: bool = Field(default=False, description="Whether this is a review evaluation (lighter assessment)")

    class Config:
        json_schema_extra = {
            "example": {
                "step_type": "what",
                "knowledge_point_title": "OSI七层模型",
                "user_input": "OSI模型将网络通信分为七个层次...",
                "knowledge_point_content": "OSI参考模型...",
            }
        }


class EvaluateResponse(BaseModel):
    """Response model for non-streaming evaluation."""
    score: int = Field(..., ge=0, le=100, description="Evaluation score")
    feedback: str = Field(..., description="AI feedback in Chinese")
    follow_up_question: str = Field(..., description="Follow-up question in Chinese")


class SearchRequest(BaseModel):
    """Request model for AI search endpoint."""
    topic: str = Field(..., description="Search topic for knowledge points")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: str = ""


# API Endpoints
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "three-question-study-machine",
        "version": "1.0.0",
        "deepseek_model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
    }


@app.post("/api/v1/evaluate")
async def evaluate_answer(request: EvaluateRequest):
    """
    Evaluate a student's answer using DeepSeek AI.

    This endpoint returns a complete JSON response (non-streaming).
    Use /api/v1/evaluate/stream for SSE streaming responses.
    """
    start_time = time.time()
    logger.info(
        f"Evaluate request: step={request.step_type}, "
        f"kp={request.knowledge_point_title}, "
        f"input_length={len(request.user_input)}"
    )

    # Validate step type
    valid_steps = ["what", "why", "how", "review"]
    if request.step_type not in valid_steps:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid step_type. Must be one of: {valid_steps}",
        )

    try:
        result = await deepseek_client.evaluate(
            step_type=request.step_type,
            knowledge_point_title=request.knowledge_point_title,
            user_input=request.user_input,
            knowledge_point_content=request.knowledge_point_content,
            follow_up_context=request.follow_up_context,
            review_mode=request.review_mode,
        )

        elapsed = time.time() - start_time
        logger.info(f"Evaluation completed in {elapsed:.2f}s, score={result.get('score', 'N/A')}")

        return EvaluateResponse(
            score=result.get("score", 60),
            feedback=result.get("feedback", "评价完成"),
            follow_up_question=result.get("follow_up_question", ""),
        )

    except Exception as e:
        logger.error(f"Evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/evaluate/stream")
async def evaluate_stream(request: EvaluateRequest):
    """
    Stream AI evaluation response using SSE.

    Returns tokens progressively for real-time display in the frontend.
    Each SSE event follows format: event: token, data: {text_chunk}
    """
    logger.info(
        f"Stream evaluate request: step={request.step_type}, "
        f"kp={request.knowledge_point_title}"
    )

    # Validate step type
    valid_steps = ["what", "why", "how", "review"]
    if request.step_type not in valid_steps:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid step_type. Must be one of: {valid_steps}",
        )

    async def event_generator():
        """Generate SSE events from DeepSeek stream."""
        try:
            accumulated = ""
            async for token in deepseek_client.evaluate_stream(
                step_type=request.step_type,
                knowledge_point_title=request.knowledge_point_title,
                user_input=request.user_input,
                knowledge_point_content=request.knowledge_point_content,
                follow_up_context=request.follow_up_context,
                review_mode=request.review_mode,
            ):
                # Check for error messages
                try:
                    parsed = json.loads(token)
                    if parsed.get("error"):
                        yield {
                            "event": "error",
                            "data": json.dumps(parsed),
                        }
                        return
                except json.JSONDecodeError:
                    pass

                accumulated += token
                yield {
                    "event": "token",
                    "data": token,
                }

            # Send complete event with full accumulated response
            yield {
                "event": "complete",
                "data": accumulated,
            }

        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield {
                "event": "error",
                "data": json.dumps({"error": True, "message": str(e)}),
            }

    return EventSourceResponse(event_generator())


@app.post("/api/v1/search")
async def search_knowledge_points(request: SearchRequest):
    """
    AI-powered search for knowledge points related to a topic.

    Returns suggested knowledge points with titles and content.
    """
    logger.info(f"Search request: topic={request.topic}")

    prompt = (
        f"Generate 5-10 knowledge points about '{request.topic}' for a study course. "
        f"For each knowledge point, provide a title and a brief reference content (2-3 sentences). "
        f"Return JSON array: [{{\"title\": \"Chinese text\", \"content\": \"Chinese text\"}}]"
    )

    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "messages": [
            {"role": "system", "content": "You are a helpful educational content generator. Generate knowledge points in Chinese."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.8,
        "max_tokens": 800,
    }

    try:
        import httpx
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')}/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="AI search service error",
                )

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Try to parse JSON from response
            try:
                knowledge_points = json.loads(content)
                return {"knowledge_points": knowledge_points}
            except json.JSONDecodeError:
                # Extract JSON array from text
                import re
                match = re.search(r'\[.*\]', content, re.DOTALL)
                if match:
                    try:
                        knowledge_points = json.loads(match.group())
                        return {"knowledge_points": knowledge_points}
                    except json.JSONDecodeError:
                        pass

                return {"knowledge_points": [], "raw_content": content}

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Search request timeout")
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="request_error",
            detail=str(exc.detail),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="server_error",
            detail="An unexpected error occurred",
        ).model_dump(),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Listen on all interfaces for emulator access
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )