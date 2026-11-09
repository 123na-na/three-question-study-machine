## ADDED Requirements

### Requirement: Learning Report Generation
The system SHALL generate a comprehensive learning report for each completed knowledge point, including mastery scores, AI feedback summaries, and full dialogue transcripts.

#### Scenario: Generate report for completed knowledge point
- **WHEN** user completes all three steps (What, Why, How) for a knowledge point
- **THEN** system generates learning report with: course name, knowledge point title, individual step scores, overall mastery score, AI feedback for each step, full dialogue transcript

#### Scenario: Display report summary
- **WHEN** user views a learning report
- **THEN** system displays summary section showing: overall score badge, completion date, time spent learning

#### Scenario: Display step-by-step breakdown
- **WHEN** user views learning report details
- **THEN** system shows three sections (What/Why/How) with: step score, AI feedback text, user's original answer, follow-up question from AI

#### Scenario: Display full dialogue transcript
- **WHEN** user scrolls to transcript section of report
- **THEN** system displays timestamped conversation history showing: user answer submission, AI evaluation response, timestamps for each turn

---

### Requirement: Report Export to Text File
The system SHALL allow users to export learning reports as plain text files for assignment submission (MVP scope).

#### Scenario: Export single knowledge point report
- **WHEN** user clicks "Export Report" button on a learning report page
- **THEN** system generates plain text file with formatted report content AND saves to device Documents folder

#### Scenario: Export multiple reports
- **WHEN** user selects multiple completed knowledge points AND clicks "Batch Export"
- **THEN** system generates single text file containing all selected reports with section dividers

#### Scenario: Text file content structure
- **WHEN** text file is generated
- **THEN** file includes: (1) Header with course name and knowledge point title, (2) Score summary, (3) Detailed feedback per step, (4) Full dialogue transcript with timestamps

#### Scenario: Text file naming
- **WHEN** text file is saved
- **THEN** system names file as: `{course_name}_{knowledge_point_title}_{timestamp}.txt`

---

### Requirement: Dialogue Record Storage
The system SHALL store complete dialogue records for every learning session, including user answers, AI evaluations, and timestamps.

#### Scenario: Record user answer
- **WHEN** user submits answer for any step
- **THEN** system stores user answer text in RDB with timestamp and session ID

#### Scenario: Record AI evaluation
- **WHEN** AI evaluation response is received
- **THEN** system stores AI feedback, score, and follow-up question in RDB linked to the same session ID

#### Scenario: Retrieve dialogue history
- **WHEN** user opens learning report
- **THEN** system retrieves and displays all dialogue turns for that knowledge point in chronological order

---

### Requirement: Mastery Assessment Criteria
The system SHALL calculate mastery scores using weighted criteria based on AI evaluation across all three steps.

#### Scenario: Calculate weighted mastery score
- **WHEN** all three steps are completed
- **THEN** system calculates overall score using weights: What (30%) + Why (35%) + How (35%)

#### Scenario: Mastery level classification
- **WHEN** overall mastery score is calculated
- **THEN** system assigns mastery level: "Excellent" (90-100), "Good" (75-89), "Satisfactory" (60-74), "Needs Review" (below 60)

#### Scenario: Display mastery level badge
- **WHEN** user views report
- **THEN** system displays colored badge indicating mastery level (green for Excellent, blue for Good, orange for Satisfactory, red for Needs Review)

---

### Requirement: Error Handling for Report Generation
The system SHALL handle errors gracefully when generating or exporting learning reports.

#### Scenario: Export failure due to storage error
- **WHEN** system fails to write export file to device storage
- **THEN** system shows error "Export failed. Please check available storage space." AND retains report in memory for retry

#### Scenario: Incomplete report for partially completed knowledge point
- **WHEN** user attempts to view report for knowledge point with only 1 or 2 completed steps
- **THEN** system shows "Learning not complete. X/3 steps completed." AND disables export button
