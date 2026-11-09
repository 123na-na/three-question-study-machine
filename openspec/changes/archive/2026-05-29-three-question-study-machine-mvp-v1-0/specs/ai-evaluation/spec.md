## ADDED Requirements

### Requirement: AI Evaluation via Backend Middleware
The system SHALL send user answers to backend middleware, which SHALL call DeepSeek API and return structured evaluation results including score, feedback, and follow-up question.

#### Scenario: Submit answer for evaluation
- **WHEN** user submits answer in any step (What/Why/How)
- **THEN** system sends POST request to backend `/api/evaluate` endpoint with user answer, knowledge point content, and step type

#### Scenario: Receive structured evaluation
- **WHEN** backend returns evaluation response
- **THEN** system parses JSON response containing: `score` (0-100), `feedback` (Chinese text), `follow_up_question` (Chinese text)

#### Scenario: Display evaluation result
- **WHEN** evaluation response is received
- **THEN** system displays AI feedback with score badge, detailed feedback text, and follow-up question

#### Scenario: Evaluation error handling
- **WHEN** backend returns error (HTTP 4xx/5xx) or timeout
- **THEN** system shows error message "Evaluation failed. Please retry." AND keeps answer in input field for resubmission

---

### Requirement: SSE Streaming Response Display
The system SHALL display AI evaluation responses progressively using Server-Sent Events (SSE) streaming, showing text character-by-character as it arrives.

#### Scenario: Stream AI response
- **WHEN** AI starts generating evaluation response
- **THEN** system displays tokens progressively in real-time (character-by-character or word-by-word)

#### Scenario: SSE event format
- **WHEN** backend sends SSE events
- **THEN** each event follows format: `event: token\ndata: {text_chunk}\n\n`

#### Scenario: Streaming completion indicator
- **WHEN** SSE stream ends (AI finishes generating)
- **THEN** system shows "Complete" indicator and enables "Next Step" or "Proceed" button

#### Scenario: Streaming interruption
- **WHEN** network connection is lost during streaming
- **THEN** system shows "Connection interrupted" message AND provides "Retry" button

#### Scenario: Streaming timeout handling
- **WHEN** no SSE events received for 30 seconds
- **THEN** system shows "AI is thinking..." message AND continues waiting up to 120 seconds total

#### Scenario: Streaming cancellation
- **WHEN** user clicks "Cancel" during streaming
- **THEN** system aborts SSE connection AND discards partial response AND returns to input state

---

### Requirement: AI Evaluation Prompt Template
The system SHALL use structured prompt templates for AI evaluation to ensure consistent response format and reduce hallucination risk.

#### Scenario: Prompt template for What step
- **WHEN** system constructs prompt for "What" step evaluation
- **THEN** system uses template: "You are a patient, encouraging learning assistant. Evaluate the student's answer to 'What is [knowledge_point_title]?'. Student answer: {user_input}. Reference content: {knowledge_point_content}. Return JSON: {{\"score\": 0-100, \"feedback\": \"Chinese text\", \"follow_up_question\": \"Chinese text\"}}"

#### Scenario: Prompt template for Why step
- **WHEN** system constructs prompt for "Why" step evaluation
- **THEN** system uses template: "You are a patient, encouraging learning assistant. Evaluate the student's answer to 'Why does [knowledge_point_title] work this way?'. Student answer: {user_input}. Reference content: {knowledge_point_content}. Return JSON: {{\"score\": 0-100, \"feedback\": \"Chinese text\", \"follow_up_question\": \"Chinese text\"}}"

#### Scenario: Prompt template for How step
- **WHEN** system constructs prompt for "How" step evaluation
- **THEN** system uses template: "You are a patient, encouraging learning assistant. Evaluate the student's answer to 'How to apply [knowledge_point_title] in practice?'. Student answer: {user_input}. Reference content: {knowledge_point_content}. Return JSON: {{\"score\": 0-100, \"feedback\": \"Chinese text\", \"follow_up_question\": \"Chinese text\"}}"

#### Scenario: Handle non-JSON AI response
- **WHEN** AI returns response that is not valid JSON
- **THEN** system shows error "Evaluation format error. Please retry." AND logs raw response for debugging

---

### Requirement: Single-Turn Evaluation with Follow-Up Option
The system SHALL provide single-turn AI evaluation per step (MVP scope), with a reserved UI element for future multi-turn follow-up questions.

#### Scenario: Single-turn evaluation flow
- **WHEN** user submits answer AND AI evaluation completes
- **THEN** system displays evaluation result AND shows "Proceed to Next Step" button as primary action

#### Scenario: Follow-up question placeholder
- **WHEN** evaluation result is displayed
- **THEN** system shows a grayed-out "Ask Follow-Up" button (disabled, labeled "Coming Soon") for future multi-turn support

#### Scenario: Display follow-up question from AI
- **WHEN** AI evaluation includes a follow-up question in response
- **THEN** system displays the follow-up question below the feedback as a learning prompt (not interactive in MVP)

---

### Requirement: Evaluation Score Calculation
The system SHALL calculate and store mastery scores based on AI evaluation across all three steps for each knowledge point.

#### Scenario: Calculate weighted mastery score
- **WHEN** all three steps (What, Why, How) have been completed with AI evaluations
- **THEN** system calculates overall score using weights: What (30%) + Why (35%) + How (35%)

#### Scenario: Store individual step scores
- **WHEN** AI evaluation completes for any step
- **THEN** system stores the step score in RDB linked to the learning session record

#### Scenario: Display score breakdown
- **WHEN** user views learning report for a knowledge point
- **THEN** system displays individual scores for What, Why, and How steps alongside weighted overall score
