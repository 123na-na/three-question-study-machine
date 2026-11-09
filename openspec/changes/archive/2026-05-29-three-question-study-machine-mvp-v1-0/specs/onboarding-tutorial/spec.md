## ADDED Requirements

### Requirement: First-Use Onboarding Tutorial
The system SHALL display an interactive tutorial on first launch to guide users through the Three-Question learning flow.

#### Scenario: Detect first launch
- **WHEN** user opens app for the first time AND `has_completed_onboarding` flag is false
- **THEN** system displays onboarding tutorial overlay

#### Scenario: Tutorial walkthrough
- **WHEN** user is in onboarding tutorial
- **THEN** system shows step-by-step guide: (1) How to select a course, (2) How to answer What/Why/How questions, (3) How to view reports

#### Scenario: Complete onboarding
- **WHEN** user finishes tutorial walkthrough AND clicks "Get Started"
- **THEN** system sets `has_completed_onboarding` flag to true AND navigates to home page

#### Scenario: Skip onboarding
- **WHEN** user clicks "Skip Tutorial" button
- **THEN** system sets `has_completed_onboarding` flag to true AND navigates to home page

---

### Requirement: Pre-loaded Sample Courses
The system SHALL include 5 pre-loaded sample courses with knowledge points, bundled as JSON files in app resources.

#### Scenario: Load sample courses on first launch
- **WHEN** app launches for the first time
- **THEN** system reads JSON files from `resources/rawfile/sample_courses/` AND inserts courses and knowledge points into RDB

#### Scenario: Sample courses are read-only
- **WHEN** user views a pre-loaded sample course
- **THEN** system displays a "Sample Course" badge AND disables edit/delete actions for the course and its knowledge points

#### Scenario: Sample course content
- **WHEN** sample courses are loaded
- **THEN** system includes these 5 courses: Computer Networks, Marxist Principles, Python Programming Basics, Calculus I, How to Use This App

---

### Requirement: Sample Course Knowledge Point Content
Each sample course SHALL include predefined knowledge points with titles and reference content for AI evaluation.

#### Scenario: Computer Networks sample course
- **WHEN** Computer Networks course is loaded
- **THEN** system includes knowledge points such as: "OSI Seven-Layer Model", "TCP Three-Way Handshake", "IP Addressing", "DNS Resolution", etc. (minimum 10 knowledge points)

#### Scenario: Marxist Principles sample course
- **WHEN** Marxist Principles course is loaded
- **THEN** system includes knowledge points such as: "Dialectical Materialism", "Historical Materialism", "Surplus Value Theory", etc. (minimum 8 knowledge points)

#### Scenario: Python Programming Basics sample course
- **WHEN** Python Programming Basics course is loaded
- **THEN** system includes knowledge points such as: "Variables and Data Types", "Control Flow", "Functions", "Object-Oriented Programming", etc. (minimum 12 knowledge points)

#### Scenario: Calculus I sample course
- **WHEN** Calculus I course is loaded
- **THEN** system includes knowledge points such as: "Limits and Continuity", "Derivatives", "Integration", "Fundamental Theorem of Calculus", etc. (minimum 10 knowledge points)

#### Scenario: How to Use This App tutorial course
- **WHEN** How to Use This App course is loaded
- **THEN** system includes knowledge points such as: "Creating a Course", "Answering What Questions", "Understanding AI Feedback", "Viewing Progress Reports", etc. (minimum 5 knowledge points)
