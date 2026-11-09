## ADDED Requirements

### Requirement: Generate certificate on course completion
The system SHALL generate a completion certificate when the user completes all knowledge points in a course (all three steps for each KP with "completed" status).

#### Scenario: Certificate generation
- **WHEN** all knowledge points in a course have all three steps completed
- **THEN** the system SHALL generate a certificate with the course name, completion date, and overall score

#### Scenario: Certificate display
- **WHEN** the user views a completed course
- **THEN** the system SHALL display a certificate option
