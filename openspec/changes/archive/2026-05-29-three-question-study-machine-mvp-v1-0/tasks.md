# Tasks: Three-Question Study Machine MVP v1.0

## Phase 1: Frontend Core (Week 1-2)

### 1.1 Project Structure Setup
- [x] Create page routing structure: `pages/Index.ets`, `pages/CourseList.ets`, `pages/LearningSession.ets`, `pages/LearningReport.ets`
- [x] Update `module.json5` to register new pages in `main_pages.json`
- [x] Create directory structure: `model/`, `service/`, `component/`, `utils/`, `constants/`

### 1.2 Database Schema & Storage Layer
- [x] Create RDB helper class in `service/DatabaseHelper.ets`
- [x] Define data models in `model/`:
  - `Course.ets`: id, name, description, is_sample, created_at
  - `KnowledgePoint.ets`: id, course_id, title, content, created_at
  - `LearningSession.ets`: id, knowledge_point_id, step, status, started_at, completed_at, score
  - `DialogueRecord.ets`: id, session_id, turn_index, user_input, ai_response, timestamp
- [x] Implement CRUD operations for each model
- [x] Add database initialization logic in `EntryAbility.ets`

### 1.3 Course Management UI
- [x] Create `CourseList.ets` page with scrollable course list
- [x] Implement course card component with: course name, description, progress bar, sample badge
- [x] Add "Create Course" button with dialog form (name, description)
- [x] Implement course detail page showing knowledge point list
- [x] Add knowledge point CRUD UI (add, edit, delete)
- [x] Implement sample course read-only logic (disable edit/delete for sample courses)
- [x] Add AI search button and result display for knowledge points

### 1.4 Three-Question Learning Flow UI
- [x] Create `LearningSession.ets` page with stepper component
- [x] Implement 3-step wizard UI: "1. What", "2. Why", "3. How"
- [x] Add step progress indicators (completed ✓, current ●, locked 🔒)
- [x] Create text input component with character counter (minimum 20 chars)
- [x] Implement step navigation logic (mandatory sequential progression)
- [x] Add step validation: prevent skipping incomplete steps
- [x] Implement "Submit" button with disabled state for empty input

---

## Phase 2: Backend Middleware (Week 2-3)

### 2.1 FastAPI Project Setup
- [x] Create backend directory: `backend/`
- [x] Initialize FastAPI project: `main.py`, `requirements.txt`, `.env`
- [x] Install dependencies: `fastapi`, `uvicorn`, `httpx`, `python-dotenv`
- [x] Create API endpoint structure: `/api/v1/evaluate`

### 2.2 DeepSeek API Integration
- [x] Create `backend/services/deepseek_client.py` for API calls
- [x] Implement async streaming method using `httpx`
- [x] Add error handling and retry logic for API calls
- [x] Create prompt template system for What/Why/How steps
- [x] Test API integration with sample prompts (⚠️ API Key余额不足402, 需充值后重新测试)

### 2.3 SSE Streaming Endpoint
- [x] Implement `/api/evaluate` POST endpoint
- [x] Add SSE streaming support using `EventSourceResponse`
- [x] Parse user request: knowledge_point_title, user_input, step_type, reference_content
- [x] Construct AI prompt using templates
- [x] Stream AI response tokens back to frontend
- [x] Add timeout handling (120s max, 30s heartbeat)
- [x] Implement request logging and cost tracking

### 2.4 Backend Deployment
- [ ] Create `Dockerfile` for containerization
- [x] Test local deployment with `uvicorn main:app --reload` (已验证health endpoint返回200)
- [ ] Deploy to cloud server (Aliyun/Tencent Cloud)
- [x] Configure environment variables for DeepSeek API key
- [ ] Test remote endpoint accessibility

---

## Phase 3: Integration & AI Features (Week 3-4)

### 3.1 Frontend-Backend Connection
- [x] Create `service/AIService.ets` for HTTP requests
- [ ] Implement SSE streaming parser in ArkTS
- [x] Connect "Submit" button to backend `/api/evaluate` endpoint
- [ ] Handle streaming response display (character-by-character)
- [x] Add loading states: "AI is thinking...", "Complete ✓"
- [ ] Implement retry logic for network failures

### 3.2 AI Evaluation Integration
- [x] Implement evaluation response parsing (JSON: score, feedback, follow_up_question)
- [x] Display AI feedback with score badge
- [x] Store evaluation results in RDB (LearningSession, DialogueRecord)
- [x] Implement weighted score calculation: What (30%) + Why (35%) + How (35%)
- [x] Add error handling for invalid JSON responses
- [x] Implement "Proceed to Next Step" button after evaluation

### 3.3 Onboarding Tutorial
- [x] Create onboarding overlay component with step-by-step guide
- [x] Implement first-launch detection using Preferences API (`has_completed_onboarding` flag)
- [x] Add tutorial steps: (1) Select course, (2) Answer questions, (3) View reports
- [x] Add "Skip Tutorial" and "Get Started" buttons
- [x] Implement sample course loading on first launch

### 3.4 Sample Courses Data
- [x] Create JSON files in `resources/rawfile/sample_courses/`:
  - `computer_networks.json` (10 knowledge points)
  - `marxist_principles.json` (8 knowledge points)
  - `python_basics.json` (12 knowledge points)
  - `calculus_1.json` (10 knowledge points)
  - `app_tutorial.json` (5 knowledge points)
- [x] Implement JSON parsing and RDB insertion logic
- [ ] Test sample course display and read-only behavior

---

## Phase 4: Polish & Reporting (Week 4-5)

### 4.1 Learning Report Generation
- [x] Create `LearningReport.ets` page
- [x] Implement report display with sections: summary, step breakdown, dialogue transcript
- [x] Calculate and display mastery level: Excellent (90-100), Good (75-89), Satisfactory (60-74), Needs Review (<60)
- [x] Add colored badges for mastery levels
- [x] Display time spent learning and completion date

### 4.2 Report Export
- [x] Implement text file export functionality
- [x] Format export content: header, scores, feedback, dialogue transcript
- [x] Save to `Documents/` directory with naming: `{course}_{knowledge_point}_{timestamp}.txt`
- [ ] Add batch export for multiple knowledge points
- [x] Handle export errors (storage full, permission denied)

### 4.3 Progress Tracking Dashboard
- [x] Add progress dashboard to home page
- [x] Display overall stats: total courses, knowledge points, completed, average score
- [x] Implement per-course progress bars
- [x] Add knowledge point status indicators (completed/in-progress/not-started)
- [x] Create 30-day activity bar chart (daily learning count)
- [x] Implement streak tracking (consecutive learning days)
- [x] Add streak milestone celebrations (7, 14, 30 days)

### 4.4 Error Recovery & Polish
- [x] Implement network interruption recovery (save answer locally, retry when online)
- [ ] Add session resume logic after app crash
- [ ] Implement data validation: duplicate knowledge point titles, incomplete course deletion
- [x] Add user-friendly error messages throughout the app
- [ ] Test end-to-end user flows

### 4.5 Demo Preparation
- [ ] Record demo video showing: course creation, three-question learning, AI evaluation, report export
- [ ] Write Fix process documentation
- [ ] Test on real HarmonyOS device or emulator
- [ ] Fix any remaining bugs
- [ ] Final code review and cleanup

---

## Testing Checklist

### Unit Tests
- [ ] Database CRUD operations
- [ ] Score calculation (weighted average)
- [ ] JSON parsing for AI responses
- [ ] Character counter validation
- [ ] Step progression logic

### Integration Tests
- [ ] Frontend → Backend API call
- [ ] SSE streaming response handling
- [ ] Sample course loading on first launch
- [ ] Report generation and export
- [ ] Network error recovery

### User Acceptance Tests
- [ ] Complete three-question flow for a knowledge point
- [ ] Create new course with knowledge points
- [ ] Use AI search to add knowledge points
- [ ] Export learning report as text file
- [ ] View progress dashboard with activity chart

---

## Dependencies & Prerequisites

- [x] DeepSeek API key obtained and configured
- [ ] DevEco Studio installed and configured
- [ ] HarmonyOS SDK installed (API 10+)
- [ ] Python 3.9+ installed (for backend)
- [ ] Cloud server provisioned (for backend deployment)
- [ ] Git repository initialized

---

## Risk Mitigation

- **AI API Cost**: DeepSeek API新用户送500万免费token(30天有效), 当前Key余额不足(402 Insufficient Balance), 需充值约$8-10即可完成开发测试。费用极低(每百万token约$0.27-1.10)。实现请求缓存和速率限制(每天最多100个请求)
- **Network Dependency**: Save answers locally immediately, queue evaluations for retry
- **ArkTS Learning Curve**: Start with simple components, iterate incrementally
- **Backend Deployment**: Test with mock responses before real API integration
- **Time Constraints**: Prioritize P0 features, defer P1/P2 to future iterations