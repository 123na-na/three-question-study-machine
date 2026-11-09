## Why

College students need a systematic learning tool to achieve deep understanding of knowledge. Most existing learning apps focus only on memorization, lacking guidance for "understanding and application". The Three-Question method (What → Why → How) solves the problem of weak knowledge retention and inability to apply, but currently no digital tool supports this learning method.

## What Changes

Core Features:
1. Three-Question Learning Flow Page - Visual three-step progression (What/Why/How), text input for answers, AI evaluation and feedback
2. Course/Knowledge Point Management - Students create courses, add knowledge points manually, AI-assisted search for related content
3. AI Dialogue Evaluation System - Backend middleware calls DeepSeek API to evaluate answers, ask follow-up questions, supplement knowledge, supports SSE streaming output
4. Onboarding Tutorial + Pre-loaded Courses - 5 sample courses (Computer Networks/Marxism/Python/Calculus/App Tutorial), first-use guide for Three-Question flow
5. Learning Report & Dialogue Records - Generate mastery assessment reports, export complete dialogue transcripts (for assignment submission)
6. Learning Progress Tracking - Visualize learning progress, Three-Question completion status, knowledge mastery heatmap

Technical Stack:
- Frontend: HarmonyOS ArkTS + ArkUI declarative UI
- Backend: Python FastAPI (API middleware layer)
- AI Model: DeepSeek API
- Data Storage: HarmonyOS RDB (local) + PostgreSQL (cloud)
- Architecture: Frontend → Backend middleware → AI API

## Capabilities

### New Capabilities
- **three-question-flow**: Three-step learning process (What → Why → How) with mandatory sequential progression
- **course-management**: Course and knowledge point CRUD operations with AI-assisted content search
- **ai-evaluation**: AI-powered answer evaluation via backend middleware with SSE streaming
- **onboarding-tutorial**: First-use tutorial and 5 pre-loaded sample courses
- **learning-report**: Learning report generation with mastery scores and dialogue transcripts
- **progress-tracking**: Visual progress dashboard with activity charts and streak tracking

### Modified Capabilities
<!-- No existing capabilities modified in MVP -->

## Impact

**Affected Systems:**
- HarmonyOS ArkTS frontend (new pages, components, RDB schema)
- Python FastAPI backend (new endpoints for AI evaluation)
- DeepSeek API integration (new dependency)

**New Dependencies:**
- DeepSeek API (ai-evaluation)
- HarmonyOS RDB module (local data storage)
- HarmonyOS HTTP streaming API (SSE support)
