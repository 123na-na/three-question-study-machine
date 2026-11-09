## ADDED Requirements

### Requirement: Learning Progress Dashboard
The system SHALL provide a visual dashboard displaying user's overall learning progress across all courses and knowledge points.

#### Scenario: Display overall progress summary
- **WHEN** user opens home page
- **THEN** system displays summary cards showing: total courses, total knowledge points, completed knowledge points, average mastery score

#### Scenario: Display per-course progress
- **WHEN** user views a specific course
- **THEN** system shows progress bar indicating: completed knowledge points / total knowledge points

#### Scenario: Display per-knowledge-point status
- **WHEN** user views course knowledge point list
- **THEN** system shows status icon for each knowledge point: completed (green check), in-progress (blue clock), not-started (gray circle)

---

### Requirement: Three-Question Completion Status
The system SHALL track and display completion status for each of the three questions (What/Why/How) per knowledge point.

#### Scenario: Track step completion
- **WHEN** user completes any step (What/Why/How) with AI evaluation
- **THEN** system marks that step as "completed" in RDB with completion timestamp and score

#### Scenario: Display step completion indicators
- **WHEN** user views knowledge point in course list
- **THEN** system shows three mini indicators (one per step) showing: completed or incomplete status

#### Scenario: Calculate completion percentage
- **WHEN** user views knowledge point progress
- **THEN** system displays completion percentage: (completed steps / 3) × 100%

---

### Requirement: Learning Activity Statistics
The system SHALL display learning activity statistics showing daily learning intensity over the past 30 days (simplified bar chart for MVP).

#### Scenario: Display monthly activity chart
- **WHEN** user views progress dashboard
- **THEN** system displays simple bar chart (30 days) showing number of knowledge points learned per day

#### Scenario: Activity bar height
- **WHEN** user has varying activity levels across days
- **THEN** system shows bar height proportional to knowledge points learned that day (max height = 5+ knowledge points)

#### Scenario: Activity bar interaction
- **WHEN** user taps on a bar in the chart
- **THEN** system shows tooltip with: date, number of knowledge points learned, courses studied

---

### Requirement: Streak Tracking
The system SHALL track and display consecutive learning days to encourage consistent study habits.

#### Scenario: Track daily learning streak
- **WHEN** user completes at least one knowledge point on a given day
- **THEN** system increments streak counter

#### Scenario: Streak reset on inactivity
- **WHEN** user does not complete any knowledge point for 24+ hours
- **THEN** system resets streak counter to 0

#### Scenario: Display current streak
- **WHEN** user views progress dashboard
- **THEN** system displays "Current Streak: X days" with fire icon

#### Scenario: Streak milestone celebration
- **WHEN** user reaches streak milestones (7, 14, 30 days)
- **THEN** system displays celebration animation and congratulatory message

---

### Requirement: Progress Statistics
The system SHALL calculate and display learning statistics for user self-reflection.

#### Scenario: Display total learning time
- **WHEN** user views statistics section
- **THEN** system shows total time spent learning (sum of all learning session durations)

#### Scenario: Display average score trend
- **WHEN** user views statistics section
- **THEN** system shows line chart of average mastery scores over time (weekly aggregation)

#### Scenario: Display strongest and weakest areas
- **WHEN** user views statistics section
- **THEN** system shows: top 3 knowledge points by score (strongest), bottom 3 knowledge points by score (needs review)
