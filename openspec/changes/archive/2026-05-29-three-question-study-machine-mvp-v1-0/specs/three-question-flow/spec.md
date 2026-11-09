## ADDED Requirements

### Requirement: Three-Question Learning Flow
The system SHALL provide a structured three-step learning process (What → Why → How) for each knowledge point, with mandatory sequential progression and visual step indicators.

#### Scenario: User starts learning a knowledge point
- **WHEN** user selects a knowledge point from a course
- **THEN** system displays Step 1 (What) with AI prompt and text input field

#### Scenario: User completes What step
- **WHEN** user submits answer for "What" question AND AI evaluation is complete
- **THEN** system unlocks Step 2 (Why) and shows completion indicator for Step 1

#### Scenario: User attempts to skip steps
- **WHEN** user tries to navigate to Step 3 without completing Step 1 and Step 2
- **THEN** system blocks navigation and shows message "Complete previous steps first"

#### Scenario: All three steps completed
- **WHEN** user completes all three steps (What, Why, How)
- **THEN** system marks knowledge point as "Mastered" and unlocks learning report

---

### Requirement: Step Progress Visualization
The system SHALL display a visual stepper component showing current progress across the three questions, with clear indicators for completed, current, and locked steps.

#### Scenario: Display step progress
- **WHEN** user is on any step of the learning flow
- **THEN** system shows stepper with three labeled nodes: "1. What", "2. Why", "3. How"

#### Scenario: Completed step indicator
- **WHEN** a step has been completed with AI evaluation
- **THEN** system displays green checkmark icon and score badge on that step node

#### Scenario: Current step indicator
- **WHEN** a step is active and awaiting user input
- **THEN** system highlights that step with blue accent color and pulsing animation

#### Scenario: Locked step indicator
- **WHEN** a step is not yet accessible
- **THEN** system displays grayed-out step node with lock icon

---

### Requirement: Answer Input and Validation
The system SHALL provide text input fields for user answers with minimum length validation and character counter.

#### Scenario: Valid answer submission
- **WHEN** user enters at least 20 Chinese characters AND clicks "Submit"
- **THEN** system sends answer to AI evaluation endpoint

#### Scenario: Insufficient answer length
- **WHEN** user enters fewer than 20 Chinese characters AND clicks "Submit"
- **THEN** system shows error message "Please provide a more detailed answer (minimum 20 characters)"

#### Scenario: Character counter display
- **WHEN** user is typing in the answer field
- **THEN** system displays real-time character count (e.g., "45/20 minimum")

#### Scenario: Empty answer prevention
- **WHEN** answer field is empty
- **THEN** "Submit" button is disabled with grayed-out state

---

### Requirement: Error Recovery for Learning Session
The system SHALL provide error recovery mechanisms when network failures or app crashes occur during a learning session.

#### Scenario: Network interruption during answer submission
- **WHEN** network connection is lost while submitting answer
- **THEN** system saves answer locally AND shows "Network unavailable. Answer saved locally." AND provides "Retry When Online" button

#### Scenario: App crash during learning session
- **WHEN** app crashes or is force-closed during active learning session
- **THEN** system preserves incomplete session in RDB AND restores it when user reopens the same knowledge point

#### Scenario: Resume incomplete session
- **WHEN** user returns to a knowledge point with incomplete session
- **THEN** system shows "Resume your previous session?" dialog AND offers to continue from last completed step
