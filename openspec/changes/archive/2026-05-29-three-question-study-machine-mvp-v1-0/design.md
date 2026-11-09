# Design: Three-Question Study Machine MVP v1.0

## Context

### Background
College students struggle with deep knowledge retention. Traditional learning apps focus on memorization (flashcards, quizzes) but lack structured guidance for understanding concepts at a deeper level. The Three-Question method (What → Why → How) is a proven pedagogical approach, but no digital tool currently implements it with AI-powered evaluation.

### Current State
- Blank HarmonyOS project created with DevEco Studio
- Basic entry page template only
- No domain models, UI components, or backend infrastructure

### Constraints
- **Academic Deadline**: Must deliver working MVP with video demo and Fix process documentation
- **Platform**: Must be HarmonyOS native (ArkTS/ArkUI), not web-based PWA
- **AI Dependency**: Core functionality requires DeepSeek API (network-dependent)
- **Team Size**: Solo developer → architecture must be lean and maintainable

### Stakeholders
- **Primary Users**: College students learning university courses
- **Secondary Users**: Lifelong learners, professionals upskilling
- **Evaluator**: Course instructor grading the 60/40 split deliverables

## Goals / Non-Goals

**Goals:**
1. Implement complete Three-Question learning flow (What → Why → How) with visual step progression
2. Enable students to create courses, add knowledge points, and learn via AI-guided Q&A
3. Provide AI evaluation with SSE streaming output and conversation history
4. Generate exportable learning reports with mastery scores and raw dialogue transcripts
5. Include onboarding tutorial and 5 pre-loaded sample courses for cold-start
6. Track learning progress with visual indicators (completion status, heatmap)

**Non-Goals:**
- User authentication/account system (MVP uses local-only data)
- Multi-device sync (local RDB only, no cloud sync in MVP)
- Real-time collaboration or social features
- Offline AI evaluation (requires network for DeepSeek API)
- Custom AI model training (using pre-trained DeepSeek only)
- Payment/subscription features

## Decisions

### Decision 1: Backend Middleware Architecture
**Choice:** Python FastAPI as API middleware between frontend and DeepSeek

**Rationale:**
- DeepSeek API key must not be exposed in frontend code (security requirement for production prototype)
- FastAPI provides native SSE streaming support (required for progressive AI response display)
- Allows future features: request caching, rate limiting, analytics logging
- Python ecosystem has excellent HTTP client libraries (httpx for async streaming)

**Alternatives Considered:**
- ❌ Direct frontend-to-API calls: Simpler but exposes API key, no caching, no rate limiting
- ❌ Node.js/Express backend: Less Python AI ecosystem integration
- ❌ Serverless functions (AWS Lambda): Cold start latency would degrade streaming UX

**Trade-off:** Adds deployment complexity (requires server hosting) but enables production-ready architecture.

---

### Decision 2: AI Model Selection
**Choice:** DeepSeek API (primary)

**Rationale:**
- Strong Chinese language understanding (target audience is Chinese-speaking students)
- Competitive pricing vs. OpenAI GPT-4
- Supports SSE streaming natively
- Fast response times (~1-2s for typical responses)

**Alternatives Considered:**
- ❌ OpenAI GPT-4: Higher cost, requires VPN in China
-  Baidu Wenxin: Weaker reasoning capabilities for educational evaluation
- ❌ Local LLM (e.g., LLaMA): Too resource-intensive for mobile deployment

**Trade-off:** Vendor lock-in to DeepSeek, but abstracted via `ai_service.ets` for future multi-model support.

---

### Decision 3: Local Data Storage Strategy
**Choice:** HarmonyOS RDB (Relational Database) for all local data

**Rationale:**
- Structured data (courses, knowledge points, dialogue records) fits relational model
- RDB supports complex queries (e.g., "find all incomplete knowledge points for course X")
- Built-in HarmonyOS support, no third-party dependencies
- Atomic transactions ensure data consistency

**Data Models:**
```
Course: id, name, description, created_at, is_sample
KnowledgePoint: id, course_id, title, content, created_at
LearningSession: id, knowledge_point_id, step (what/why/how), status, started_at, completed_at
DialogueRecord: id, session_id, turn_index, user_input, ai_response, timestamp
ProgressMetric: id, knowledge_point_id, mastery_score, last_reviewed_at
```

**Alternatives Considered:**
- ❌ Preferences API: Too limited for complex relational queries
- ❌ ObjectDB: Less mature query capabilities

**Trade-off:** More schema design upfront, but enables powerful progress tracking and reporting.

---

### Decision 4: Three-Question Flow UI Pattern
**Choice:** Step-by-step wizard with mandatory sequential progression

**Rationale:**
- Pedagogically correct: "What" must be answered before "Why", which must precede "How"
- Visual step indicator (stepper component) provides clear progress feedback
- Prevents users from skipping foundational understanding
- Each step shows: AI prompt → user input → AI evaluation → proceed to next

**UI Flow:**
```
[Step 1: What] → [Step 2: Why] → [Step 3: How] → [Report Page]
  (blocked)         (blocked)       (blocked)       (unlocked after all 3)
```

**Alternatives Considered:**
- ❌ All three questions on single page: Overwhelming, loses sequential learning benefit
- ❌ Free navigation (jump between steps): Breaks pedagogical flow, confuses users

**Trade-off:** Slower learning process per knowledge point, but higher knowledge retention.

---

### Decision 5: AI Evaluation Prompt Strategy
**Choice:** Structured prompts with explicit evaluation criteria

**Rationale:**
- Consistent evaluation across different topics/courses
- Enables quantitative scoring (0-100 mastery score for reports)
- Reduces AI hallucination risk by constraining response format

**Prompt Template (Example for "What" step):**
```
You are a patient, encouraging learning assistant for college students.
Evaluate the student's answer to "What is [knowledge point]?".

Student answer: {user_input}
Reference definition: {knowledge_point_content}

Evaluate on these criteria (0-100 each):
1. Conceptual accuracy
2. Key features coverage
3. Clarity of explanation

Return JSON: {{
  "score": <overall 0-100>,
  "feedback": "<encouraging, specific feedback in Chinese>",
  "follow_up_question": "<one clarifying question to deepen understanding>"
}}
```

**Alternatives Considered:**
- ❌ Free-form AI chat: Inconsistent quality, hard to quantify progress
- ❌ Rule-based evaluation (no AI): Cannot handle diverse student answers

**Trade-off:** Requires careful prompt engineering, but enables reliable scoring and progress tracking.

---

### Decision 6: SSE Streaming Implementation
**Choice:** Server-Sent Events (SSE) for progressive AI response display

**Rationale:**
- Native HTTP-based, simpler than WebSockets for unidirectional streaming
- FastAPI has built-in SSE support via `EventSourceResponse`
- Reduces perceived latency (user sees partial responses while AI continues generating)
- Better UX than waiting for complete response (1-3s delay feels instant with streaming)

**Backend Implementation (FastAPI):**
```python
@app.post("/api/evaluate")
async def evaluate_answer(request: EvaluationRequest):
    async def event_generator():
        async for chunk in deepseek_client.stream_completion(prompt):
            yield {"event": "token", "data": chunk}
    return EventSourceResponse(event_generator())
```

**Frontend Implementation (ArkTS):**
```typescript
// Use http.request with streaming callback
http.createHttp().request(url, {
  method: 'POST',
  extraData: requestBody,
  readTimeout: 60000,
  streamingCallback: (data: ArrayBuffer) => {
    // Parse SSE event and update UI progressively
  }
})
```

**Alternatives Considered:**
- ❌ Polling: Higher latency, more server load
- ❌ WebSockets: Overkill for server-to-client only streaming

**Trade-off:** SSE is HTTP/1.1 only (no HTTP/2 multiplexing), but sufficient for single-stream use case.

---

### Decision 7: Cold Start Content Strategy
**Choice:** Pre-load 5 sample courses on first app launch

**Rationale:**
- Solves empty state problem (users need content to experience the app immediately)
- Demonstrates app capabilities across diverse subjects
- Courses chosen to appeal to broad student audience

**Sample Courses:**
1. Computer Networks (计算机网络) - 10 knowledge points
2. Marxist Principles (马克思主义基本原理) - 8 knowledge points
3. Python Programming Basics - 12 knowledge points
4. Calculus I (高等数学) - 10 knowledge points
5. How to Use This App (Tutorial) - 5 knowledge points

**Implementation:**
- JSON files bundled in `resources/rawfile/sample_courses/`
- On first launch, check if `has_completed_onboarding` flag is false
- If false, parse JSON and insert into RDB, set flag to true

**Alternatives Considered:**
- ❌ Empty state with "Create your first course" only: High friction, poor first impression
- ❌ Fetch sample courses from server: Requires network on first launch

**Trade-off:** Increases app bundle size slightly (~200KB for JSON files), but ensures instant usability.

---

### Decision 8: Learning Report Export Format
**Choice:** Plain text export (MVP) → PDF export (P1)

**Rationale:**
- Plain text export is sufficient for assignment submission in MVP phase
- HarmonyOS PDF generation API requires additional research and implementation time
- Text export can be implemented immediately with built-in file I/O capabilities
- PDF can be added in P1 phase after core features are stable

**Report Structure (MVP - Text Format):**
```
1. Header: Course name, knowledge point title, date
2. Summary: Overall mastery score, completion date, time spent
3. Per-Step Breakdown:
   - What: Score, user answer, AI feedback
   - Why: Score, user answer, AI feedback
   - How: Score, user answer, AI feedback
4. Full Dialogue Transcripts: Timestamped conversation records
```

**Implementation (MVP):**
- Generate .txt file with formatted content
- Export to `Documents/` directory
- File naming: `{course_name}_{knowledge_point_title}_{timestamp}.txt`

**Implementation (P1 - Future):**
- Upgrade to PDF generation with formatting, charts, and badges
- Use HarmonyOS PDF API or third-party library

**Alternatives Considered:**
- ❌ JSON export: Not human-readable for instructor review
- ❌ Screenshot-based report: Poor quality, not searchable
- ❌ HTML export: Requires browser to view, less portable

**Trade-off:** Text export is less visually appealing but faster to implement. PDF upgrade path is straightforward.

## Risks / Trade-offs

### Risk 1: AI Hallucination in Evaluations
**Impact:** AI may give incorrect feedback or praise wrong answers  
**Mitigation:** 
- Use structured prompts with explicit evaluation criteria
- Include reference content in every prompt (knowledge_point_content)
- Add confidence score to AI responses; flag low-confidence evaluations
- Allow users to report incorrect evaluations (future feature)

### Risk 2: API Cost Explosion
**Impact:** Uncontrolled API usage could exceed budget  
**Mitigation:**
- Implement request caching (same question + answer = cached response)
- Rate limit to max 100 requests/user/day (backend middleware)
- Log all API calls with cost estimation for monitoring
- Provide "evaluation budget" indicator in UI

### Risk 3: Network Dependency for Core Features
**Impact:** App unusable without internet connection  
**Mitigation:**
- Save user answers locally immediately (local-first architecture)
- Queue AI evaluation requests; process when network restored
- Show clear "waiting for network" state vs. "AI processing" state
- Cache sample courses locally (already bundled)

### Risk 4: Complex Three-Question Flow May Confuse Users
**Impact:** High drop-off rate during first learning session  
**Mitigation:**
- Comprehensive onboarding tutorial with interactive walkthrough
- Show progress indicator (1/3, 2/3, 3/3) at every step
- Provide example answers for first knowledge point
- Allow "skip evaluation" option for users who want to move faster

### Risk 5: HarmonyOS ArkTS Learning Curve
**Impact:** Development delays due to unfamiliar framework  
**Mitigation:**
- Start with simple UI components, iterate incrementally
- Use DevEco Studio previewer for rapid UI iteration
- Reference HarmonyOS official documentation and sample projects
- Allocate extra time for debugging ArkTS-specific issues

### Risk 6: Backend Deployment Complexity
**Impact:** Delay in testing full integration (frontend + backend)  
**Mitigation:**
- Develop backend and frontend in parallel (mock AI responses initially)
- Use Docker for backend deployment (consistent environment)
- Test with mock API responses before integrating real DeepSeek calls
- Document backend setup process thoroughly

## Migration Plan

### Phase 1: Frontend Core (Week 1-2)
1. Create page routing structure (Index → CourseList → LearningSession → Report)
2. Implement Three-Question flow UI (stepper, text input, evaluation display)
3. Set up RDB schema and local storage layer
4. Build course management UI (create, edit, delete courses/knowledge points)

### Phase 2: Backend Middleware (Week 2-3)
1. Set up FastAPI project structure
2. Implement `/api/evaluate` endpoint with DeepSeek integration
3. Add SSE streaming support
4. Deploy to cloud server (Aliyun/Tencent Cloud)

### Phase 3: Integration & AI Features (Week 3-4)
1. Connect frontend to backend API
2. Implement streaming response handling in ArkTS
3. Build AI evaluation prompt system
4. Integrate onboarding tutorial and sample courses

### Phase 4: Polish & Reporting (Week 4-5)
1. Implement learning report generation (PDF export)
2. Add progress tracking visualizations (heatmap, radar chart)
3. Test end-to-end user flows
4. Record demo video, write Fix process documentation

### Rollback Strategy
- Each phase is independently testable
- Backend API versioning (`/api/v1/...`) allows backward compatibility
- Local data export/import for data migration between versions
- Git branching strategy: `feature/frontend-core`, `feature/backend-middleware`, `feature/ai-integration`

## Open Questions

### Q1: Which DeepSeek API endpoint to use?
- **Options:** `deepseek-chat` (general) vs. `deepseek-coder` (reasoning-focused)
- **Pending:** Test both with sample educational prompts to compare quality
- **Decision needed by:** End of Week 1 (before backend implementation)

### Q2: Should AI evaluation be synchronous or asynchronous?
- **Synchronous:** User waits for AI response before proceeding (current design)
- **Asynchronous:** User can continue to next step while AI evaluates in background
- **Pending:** User testing to determine preference
- **Impact:** Affects UI design and user flow

### Q3: How to handle multi-turn conversations within one question step?
- **Current assumption:** One evaluation per step (user answers → AI evaluates → proceed)
- **Alternative:** Allow follow-up Q&A within each step (user asks clarification → AI responds)
- **Pending:** Clarify with requirements (assignment description doesn't specify)
- **Recommendation:** Start with single-turn, add multi-turn if time permits

### Q4: What is the target device for HarmonyOS deployment?
- **Options:** Phone (already configured), tablet, watch, smart screen
- **Current config:** `deviceTypes: ["phone"]`
- **Pending:** Confirm if tablet support is needed (different screen sizes affect UI layout)

### Q5: Should sample courses be editable by users?
- **Option A:** Sample courses are read-only (users can only create new courses)
- **Option B:** Sample courses are editable (users can modify pre-loaded content)
- **Recommendation:** Option A (simpler, prevents accidental data loss)
- **Pending:** User testing feedback
