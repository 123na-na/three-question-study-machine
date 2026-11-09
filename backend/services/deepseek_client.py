"""
DeepSeek API Client for AI evaluation.

Handles communication with DeepSeek API including:
- Streaming response generation
- Prompt template construction
- Error handling and retry logic
"""

import httpx
import json
import logging
import os
from typing import AsyncGenerator, List

logger = logging.getLogger(__name__)

# Load environment variables
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# Prompt templates for each step (Chinese + strict JSON format)
PROMPT_TEMPLATES = {
    "what": (
        "你是一个耐心、鼓励性的学习助手，专门帮助中国学生深入理解知识。\n"
        "请评估学生对\"{knowledge_point_title}\"这个知识点的\"是什么\"层面的回答。\n"
        "\n"
        "学生回答: {user_input}\n"
        "参考内容: {knowledge_point_content}\n"
        "\n"
        "## 结构化评分维度（总分100分）\n"
        "\n"
        "### 1. 准确性（0-30分）\n"
        "- 概念定义是否准确、严谨\n"
        "- 是否存在知识性错误或误解\n"
        "- 关键术语使用是否正确\n"
        "\n"
        "### 2. 完整性（0-25分）\n"
        "- 是否涵盖了该概念的核心要素\n"
        "- 是否提到了关键特征和边界条件\n"
        "- 是否有重要遗漏\n"
        "\n"
        "### 3. 条理性（0-20分）\n"
        "- 表达是否清晰、有逻辑\n"
        "- 结构是否合理，是否容易理解\n"
        "- 语言是否流畅、简洁\n"
        "\n"
        "### 4. 理解深度（0-25分）\n"
        "- 是否有自己的理解和提炼，而非简单复述\n"
        "- 是否能指出本质特征\n"
        "- 是否能区分相似概念\n"
        "\n"
        "根据以上四个维度分别打分后计算总分，然后转换为最终评分。\n"
        "学生回答不足30字时应适当扣分。\n"
        "\n"
        "## 输出要求\n"
        "feedback需包含：整体评价 → 各维度具体表现 → 改进建议（具体可操作）。\n"
        "追问需与当前回答紧密相关，引导学生深入思考概念的某个方面。\n"
        "\n"
        "重要: 你必须严格只返回以下JSON格式，不要包含任何其他文字、解释或代码标记:\n"
        "{{\"score\": 0-100整数, \"feedback\": \"中文反馈（含各维度评价）\", \"follow_up_question\": \"中文追问\"}}"
    ),
    "why": (
        "你是一个耐心、鼓励性的学习助手，专门帮助中国学生深入理解知识。\n"
        "请评估学生对\"{knowledge_point_title}\"这个知识点\"为什么\"层面的回答。\n"
        "\n"
        "学生回答: {user_input}\n"
        "参考内容: {knowledge_point_content}\n"
        "\n"
        "## 结构化评分维度（总分100分）\n"
        "\n"
        "### 1. 因果逻辑（0-30分）\n"
        "- 是否准确理解因果关系，逻辑链条是否清晰\n"
        "- 是否区分了原因和结果\n"
        "- 是否存在逻辑跳跃或错误推理\n"
        "\n"
        "### 2. 原理阐述（0-25分）\n"
        "- 是否清晰解释了根本原理和内在机制\n"
        "- 是否触及了本质而非停留在表面\n"
        "- 原理表述是否准确\n"
        "\n"
        "### 3. 批判性思维（0-25分）\n"
        "- 是否有分析、比较、质疑等高阶思维活动\n"
        "- 是否能从不同角度审视问题\n"
        "- 是否有独立见解而非照本宣科\n"
        "\n"
        "### 4. 关联能力（0-20分）\n"
        "- 是否能联系其他相关知识或领域\n"
        "- 是否能说明知识点之间的联系\n"
        "- 是否能举出适当的例子佐证\n"
        "\n"
        "根据以上四个维度分别打分后计算总分，然后转换为最终评分。\n"
        "学生回答不足30字时应适当扣分。\n"
        "\n"
        "## 输出要求\n"
        "feedback需包含：整体评价 → 各维度具体表现 → 改进建议（具体可操作）。\n"
        "追问需引导学生深入思考原理的某个方面或拓展到更广泛的知识关联。\n"
        "\n"
        "重要: 你必须严格只返回以下JSON格式，不要包含任何其他文字、解释或代码标记:\n"
        "{{\"score\": 0-100整数, \"feedback\": \"中文反馈（含各维度评价）\", \"follow_up_question\": \"中文追问\"}}"
    ),
    "how": (
        "你是一个耐心、鼓励性的学习助手，专门帮助中国学生深入理解知识。\n"
        "请评估学生对\"{knowledge_point_title}\"这个知识点\"怎么用\"层面的回答。\n"
        "\n"
        "学生回答: {user_input}\n"
        "参考内容: {knowledge_point_content}\n"
        "\n"
        "## 结构化评分维度（总分100分）\n"
        "\n"
        "### 1. 场景识别（0-25分）\n"
        "- 是否准确识别了正确的应用场景\n"
        "- 是否能区分适用与不适用的场景\n"
        "- 场景描述是否具体、真实\n"
        "\n"
        "### 2. 方法掌握（0-25分）\n"
        "- 是否理解具体的使用步骤和方法\n"
        "- 操作过程描述是否清晰、可行\n"
        "- 是否注意到使用中的注意事项\n"
        "\n"
        "### 3. 实践性（0-25分）\n"
        "- 是否有实际可行、具体可操作的实施方案\n"
        "- 是否考虑了实际环境中的约束条件\n"
        "- 方案是否具有可执行性\n"
        "\n"
        "### 4. 创新性（0-25分）\n"
        "- 是否有拓展、联想和举一反三\n"
        "- 是否能创造性地运用在非典型场景\n"
        "- 是否有新颖的应用角度\n"
        "\n"
        "根据以上四个维度分别打分后计算总分，然后转换为最终评分。\n"
        "学生回答不足30字时应适当扣分。\n"
        "\n"
        "## 输出要求\n"
        "feedback需包含：整体评价 → 各维度具体表现 → 改进建议（具体可操作）。\n"
        "追问需引导学生思考更广泛的应用场景或更深入的操作细节。\n"
        "\n"
        "重要: 你必须严格只返回以下JSON格式，不要包含任何其他文字、解释或代码标记:\n"
        "{{\"score\": 0-100整数, \"feedback\": \"中文反馈（含各维度评价）\", \"follow_up_question\": \"中文追问\"}}"
    ),
}

# Follow-up prompt templates for each step (includes conversation history)
FOLLOW_UP_PROMPT = {
    "what": (
        "你是一个耐心、鼓励性的学习助手，专门帮助中国学生深入理解知识。\n"
        "这是对\"{knowledge_point_title}\"这个知识点的\"是什么\"层面的追问环节。\n"
        "\n"
        "讨论历史:\n"
        "{follow_up_context}\n"
        "\n"
        "学生对追问的回答: {user_input}\n"
        "参考内容: {knowledge_point_content}\n"
        "\n"
        "## 结构化评分维度（总分100分）\n"
        "\n"
        "### 1. 准确性（0-30分）\n"
        "- 回应是否准确、切题\n"
        "- 是否存在知识性错误\n"
        "\n"
        "### 2. 思考深度（0-30分）\n"
        "- 是否有比之前更深入的理解\n"
        "- 是否能发现新的角度\n"
        "\n"
        "### 3. 表达逻辑（0-20分）\n"
        "- 表达是否清晰、有条理\n"
        "\n"
        "### 4. 进步程度（0-20分）\n"
        "- 相比第一轮回答是否有明显进步\n"
        "- 是否吸收了之前的反馈建议\n"
        "\n"
        "根据以上维度评分后计算总分。\n"
        "\n"
        "## 输出要求\n"
        "feedback需包含：对追问回答的评价 → 指出进步或不足 → 进一步建议。\n"
        "追问需引导学生继续深入。\n"
        "\n"
        "重要: 你必须严格只返回以下JSON格式:\n"
        "{{\"score\": 0-100整数, \"feedback\": \"中文反馈\", \"follow_up_question\": \"中文追问\"}}"
    ),
    "why": (
        "你是一个耐心、鼓励性的学习助手，专门帮助中国学生深入理解知识。\n"
        "这是对\"{knowledge_point_title}\"这个知识点的\"为什么\"层面的追问环节。\n"
        "\n"
        "讨论历史:\n"
        "{follow_up_context}\n"
        "\n"
        "学生对追问的回答: {user_input}\n"
        "参考内容: {knowledge_point_content}\n"
        "\n"
        "## 结构化评分维度（总分100分）\n"
        "\n"
        "### 1. 因果逻辑（0-30分）\n"
        "- 回应是否准确理解因果关系\n"
        "\n"
        "### 2. 批判性思维（0-30分）\n"
        "- 是否有更深入的分析和思考\n"
        "- 是否从新角度审视问题\n"
        "\n"
        "### 3. 表达清晰度（0-20分）\n"
        "- 表达是否清晰、有逻辑\n"
        "\n"
        "### 4. 进步程度（0-20分）\n"
        "- 相比第一轮回答是否有明显进步\n"
        "\n"
        "根据以上维度评分后计算总分。\n"
        "\n"
        "## 输出要求\n"
        "feedback需包含：对追问回答的评价 → 指出进步或不足 → 进一步建议。\n"
        "追问需引导学生继续深入。\n"
        "\n"
        "重要: 你必须严格只返回以下JSON格式:\n"
        "{{\"score\": 0-100整数, \"feedback\": \"中文反馈\", \"follow_up_question\": \"中文追问\"}}"
    ),
    "how": (
        "你是一个耐心、鼓励性的学习助手，专门帮助中国学生深入理解知识。\n"
        "这是对\"{knowledge_point_title}\"这个知识点的\"怎么用\"层面的追问环节。\n"
        "\n"
        "讨论历史:\n"
        "{follow_up_context}\n"
        "\n"
        "学生对追问的回答: {user_input}\n"
        "参考内容: {knowledge_point_content}\n"
        "\n"
        "## 结构化评分维度（总分100分）\n"
        "\n"
        "### 1. 场景应用（0-30分）\n"
        "- 回应是否准确识别应用场景\n"
        "\n"
        "### 2. 实践性（0-30分）\n"
        "- 回答是否具体、可操作\n"
        "\n"
        "### 3. 创新性（0-20分）\n"
        "- 是否有新的应用角度\n"
        "\n"
        "### 4. 进步程度（0-20分）\n"
        "- 相比第一轮回答是否有明显进步\n"
        "\n"
        "根据以上维度评分后计算总分。\n"
        "\n"
        "## 输出要求\n"
        "feedback需包含：对追问回答的评价 → 指出进步或不足 → 进一步建议。\n"
        "追问需引导学生继续深入。\n"
        "\n"
        "重要: 你必须严格只返回以下JSON格式:\n"
        "{{\"score\": 0-100整数, \"feedback\": \"中文反馈\", \"follow_up_question\": \"中文追问\"}}"
    ),
}

# Review mode prompt (lighter evaluation for spaced repetition review)
REVIEW_PROMPT = (
    "你是一个耐心、鼓励性的学习助手，专门帮助中国学生巩固知识。\n"
    "这是对\"{knowledge_point_title}\"这个知识点的复习回顾。\n"
    "\n"
    "学生回忆内容: {user_input}\n"
    "参考内容: {knowledge_point_content}\n"
    "\n"
    "## 轻量化评分维度（总分100分）\n"
    "\n"
    "### 1. 回忆准确性（0-40分）\n"
    "- 核心概念是否准确\n"
    "- 是否存在知识性错误\n"
    "\n"
    "### 2. 理解保留度（0-30分）\n"
    "- 是否保持了最初学习的理解深度\n"
    "- 能否用自己的话清晰表达\n"
    "\n"
    "### 3. 完整性（0-30分）\n"
    "- 是否涵盖了三问（是什么、为什么、怎么用）的核心要点\n"
    "- 是否需要提醒才能记起\n"
    "\n"
    "根据以上维度评分后计算总分。注意这是复习评估，评分标准应比初次学习略宽松。\n"
    "\n"
    "## 输出要求\n"
    "feedback需包含：整体评价 → 哪里记得好 → 哪里需要加强。\n"
    "follow_up_question设为空字符串\"\"。\n"
    "\n"
    "重要: 你必须严格只返回以下JSON格式:\n"
    "{{\"score\": 0-100整数, \"feedback\": \"中文反馈\", \"follow_up_question\": \"\"}}"
)

# Fallback prompt for non-standard step types (Chinese + strict JSON)
FALLBACK_PROMPT = (
    "你是一个耐心、鼓励性的学习助手，专门帮助中国学生深入理解知识。\n"
    "请评估学生对\"{knowledge_point_title}\"的回答。\n"
    "学生回答: {user_input}\n"
    "参考内容: {knowledge_point_content}\n"
    "\n"
    "评估要求:\n"
    "1. 评分(0-100)\n"
    "2. 中文反馈\n"
    "3. 中文追问\n"
    "\n"
    "重要: 你必须严格只返回以下JSON格式，不要包含任何其他文字:\n"
    "{{\"score\": 0-100整数, \"feedback\": \"中文反馈\", \"follow_up_question\": \"中文追问\"}}"
)


class DeepSeekClient:
    """Client for interacting with DeepSeek API."""

    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.base_url = DEEPSEEK_BASE_URL
        self.model = DEEPSEEK_MODEL
        self.timeout = 120.0  # seconds

    def _build_prompt(
        self,
        step_type: str,
        knowledge_point_title: str,
        user_input: str,
        knowledge_point_content: str,
        follow_up_context: str = "",
        review_mode: bool = False,
    ) -> str:
        """Build evaluation prompt based on step type."""
        if review_mode or step_type == "review":
            return REVIEW_PROMPT.format(
                knowledge_point_title=knowledge_point_title,
                user_input=user_input,
                knowledge_point_content=knowledge_point_content,
            )
        if follow_up_context:
            template = FOLLOW_UP_PROMPT.get(step_type, FALLBACK_PROMPT)
        else:
            template = PROMPT_TEMPLATES.get(step_type, FALLBACK_PROMPT)
        return template.format(
            knowledge_point_title=knowledge_point_title,
            user_input=user_input,
            knowledge_point_content=knowledge_point_content,
            follow_up_context=follow_up_context,
        )

    async def evaluate_stream(
        self,
        step_type: str,
        knowledge_point_title: str,
        user_input: str,
        knowledge_point_content: str,
        follow_up_context: str = "",
        review_mode: bool = False,
    ) -> AsyncGenerator[str, None]:
        """
        Stream AI evaluation response using DeepSeek API.

        Returns tokens progressively for SSE streaming.
        """
        prompt = self._build_prompt(
            step_type, knowledge_point_title, user_input, knowledge_point_content, follow_up_context, review_mode
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": '你是一个耐心、鼓励性的学习助手，专门帮助中国学生。你必须严格返回纯JSON格式，不要包含任何额外的文字、解释或代码块标记。只返回如下格式: {"score": 0-100整数, "feedback": "中文反馈", "follow_up_question": "中文追问"}'},
                {"role": "user", "content": prompt},
            ],
            "stream": True,
            "temperature": 0.8,
            "max_tokens": 800,
        }

        logger.info(f"Sending evaluation request for step: {step_type}, kp: {knowledge_point_title}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/v1/chat/completions",
                    headers=headers,
                    json=payload,
                ) as response:
                    if response.status_code != 200:
                        error_body = await response.aread()
                        logger.error(f"DeepSeek API error: {response.status_code} - {error_body}")
                        yield json.dumps({
                            "error": True,
                            "message": f"AI API error: {response.status_code}",
                        })
                        return

                    async for line in response.iter_lines():
                        if not line.strip():
                            continue

                        if line.startswith("data: "):
                            data = line[6:]  # Remove "data: " prefix

                            if data == "[DONE]":
                                logger.info("Stream completed")
                                return

                            try:
                                chunk = json.loads(data)
                                content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to parse chunk: {data}")
                                continue

            except httpx.TimeoutException:
                logger.error("DeepSeek API timeout")
                yield json.dumps({
                    "error": True,
                    "message": "AI evaluation timeout. Please retry.",
                })
            except httpx.ConnectError:
                logger.error("DeepSeek API connection error")
                yield json.dumps({
                    "error": True,
                    "message": "Cannot connect to AI service. Please check network.",
                })
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                yield json.dumps({
                    "error": True,
                    "message": f"Evaluation error: {str(e)}",
                })

    async def evaluate(
        self,
        step_type: str,
        knowledge_point_title: str,
        user_input: str,
        knowledge_point_content: str,
        follow_up_context: str = "",
        review_mode: bool = False,
    ) -> dict:
        """
        Non-streaming evaluation (direct API call, no streaming).

        Used for testing and as fallback.
        """
        prompt = self._build_prompt(
            step_type, knowledge_point_title, user_input, knowledge_point_content, follow_up_context, review_mode
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": '你是一个耐心、鼓励性的学习助手，专门帮助中国学生。你必须严格返回纯JSON格式，不要包含任何额外的文字、解释或代码块标记。只返回如下格式: {"score": 0-100整数, "feedback": "中文反馈", "follow_up_question": "中文追问"}'},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "temperature": 0.8,
            "max_tokens": 800,
        }

        logger.info(f"Sending non-streaming evaluation for step: {step_type}, kp: {knowledge_point_title}")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=headers,
                    json=payload,
                )

                if response.status_code != 200:
                    error_body = response.text
                    logger.error(f"DeepSeek API error: {response.status_code} - {error_body}")
                    return {
                        "score": 60,
                        "feedback": f"AI服务错误({response.status_code})，请稍后重试。",
                        "follow_up_question": "请再次尝试回答这个问题。",
                    }

                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                logger.info(f"AI response: {content[:200]}")

                try:
                    parsed = json.loads(content)
                    return parsed
                except json.JSONDecodeError:
                    logger.warning(f"Non-JSON response, extracting: {content[:200]}")
                    return self._extract_json_from_text(content)

        except httpx.TimeoutException:
            logger.error("DeepSeek API timeout")
            return {
                "score": 60,
                "feedback": "AI评价超时，请稍后重试。",
                "follow_up_question": "请再次尝试回答这个问题。",
            }
        except Exception as e:
            logger.error(f"Unexpected error in evaluate: {e}")
            return {
                "score": 60,
                "feedback": f"评价出错: {str(e)}",
                "follow_up_question": "请再次尝试回答这个问题。",
            }

    async def _collect_stream(self, *args) -> List[str]:
        """Collect all stream tokens into a list."""
        tokens = []
        async for token in self.evaluate_stream(*args):
            try:
                # Check if it's an error message
                parsed = json.loads(token)
                if parsed.get("error"):
                    return [token]
            except json.JSONDecodeError:
                pass
            tokens.append(token)
        return tokens

    def _extract_json_from_text(self, text: str) -> dict:
        """Try to extract JSON object from text that may contain extra content."""
        import re

        # 1. Try to remove markdown code block wrapping
        # Handle ```json ... ``` or ``` ... ``` patterns
        md_match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        if md_match:
            try:
                return json.loads(md_match.group(1))
            except json.JSONDecodeError:
                pass

        # 2. Try to find any JSON object with "score" key
        # Use a more robust regex that handles nested braces
        # Find all {...} blocks and try to parse each
        brace_pattern = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
        for candidate in brace_pattern:
            try:
                parsed = json.loads(candidate)
                if 'score' in parsed:
                    return parsed
            except json.JSONDecodeError:
                continue

        # 3. Try the original simple pattern
        json_match = re.search(r'\{[^{}]*"score"[^{}]*\}', text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # 4. Try stripping all non-JSON text
        # Find first { and last } and try to parse what's between
        first_brace = text.find('{')
        last_brace = text.rfind('}')
        if first_brace >= 0 and last_brace > first_brace:
            try:
                return json.loads(text[first_brace:last_brace + 1])
            except json.JSONDecodeError:
                pass

        # Return default response if all extraction attempts fail
        logger.error(f"Failed to extract JSON from response: {text[:200]}")
        return {
            "score": 60,
            "feedback": "无法解析AI响应，请重新提交。",
            "follow_up_question": "请再次尝试回答这个问题。",
        }


# Singleton instance
deepseek_client = DeepSeekClient()