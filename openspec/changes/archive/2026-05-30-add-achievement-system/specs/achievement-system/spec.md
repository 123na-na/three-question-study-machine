## ADDED Requirements

### Requirement: Track streak achievements
The system SHALL track consecutive learning day streaks and award badges at milestone thresholds.

#### Scenario: 7-day streak badge
- **WHEN** the user has studied for 7 consecutive days
- **THEN** the system SHALL award the 7-day streak badge

#### Scenario: 14-day streak badge
- **WHEN** the user has studied for 14 consecutive days
- **THEN** the system SHALL award the 14-day streak badge

#### Scenario: 30-day streak badge
- **WHEN** the user has studied for 30 consecutive days
- **THEN** the system SHALL award the 30-day streak badge

### Requirement: Track mastery achievements
The system SHALL award badges when the user achieves specific mastery levels for the first time.

#### Scenario: First excellent mastery
- **WHEN** the user achieves an "优秀" (Excellent) mastery level for the first time
- **THEN** the system SHALL award the excellent mastery badge

#### Scenario: First good mastery
- **WHEN** the user achieves a "良好" (Good) mastery level for the first time
- **THEN** the system SHALL award the good mastery badge

### Requirement: Track knowledge point completion achievements
The system SHALL award badges when the user completes milestone counts of knowledge points.

#### Scenario: First knowledge point completion
- **WHEN** the user completes their 1st knowledge point
- **THEN** the system SHALL award the first knowledge point badge

#### Scenario: Multiple knowledge point milestones
- **WHEN** the user completes 5, 10, 25, and 50 knowledge points respectively
- **THEN** the system SHALL award badges at each milestone

### Requirement: Track course completion achievements
The system SHALL award badges when the user completes milestone counts of courses.

#### Scenario: First course completion
- **WHEN** the user completes their 1st course
- **THEN** the system SHALL award the first course badge

#### Scenario: Multiple course milestones
- **WHEN** the user completes 3 and 5 courses respectively
- **THEN** the system SHALL award badges at each milestone
