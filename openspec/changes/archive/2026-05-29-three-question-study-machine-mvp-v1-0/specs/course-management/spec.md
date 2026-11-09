## ADDED Requirements

### Requirement: Course Creation
The system SHALL allow users to create new courses with a name, description, and optional cover image.

#### Scenario: Create new course
- **WHEN** user clicks "Create Course" button AND fills in course name AND description
- **THEN** system creates a new course record in local RDB with unique ID and timestamp

#### Scenario: Course name validation
- **WHEN** user attempts to create course with empty name
- **THEN** system shows error message "Course name is required"

#### Scenario: Course list display
- **WHEN** user navigates to course management page
- **THEN** system displays all user-created courses and sample courses in a scrollable list

---

### Requirement: Knowledge Point Management
The system SHALL allow users to add, edit, and delete knowledge points within their own courses.

#### Scenario: Add knowledge point to user course
- **WHEN** user selects their own course AND clicks "Add Knowledge Point" AND provides title and content
- **THEN** system creates new knowledge point record linked to the course

#### Scenario: Edit knowledge point
- **WHEN** user selects a knowledge point from their own course AND modifies title or content AND saves
- **THEN** system updates the knowledge point record in local RDB

#### Scenario: Delete knowledge point
- **WHEN** user confirms deletion of a knowledge point from their own course
- **THEN** system removes the knowledge point and all associated learning sessions

#### Scenario: Cannot edit sample course knowledge points
- **WHEN** user attempts to edit or delete a knowledge point from a pre-loaded sample course
- **THEN** system shows message "Sample courses are read-only. Create your own course to edit."

---

### Requirement: AI-Assisted Content Search
The system SHALL allow users to search for knowledge points using AI-powered web search to supplement their courses.

#### Scenario: Search for knowledge points
- **WHEN** user enters a course topic (e.g., "Computer Networks") AND clicks "AI Search"
- **THEN** system sends search query to backend middleware AND displays AI-returned knowledge points list

#### Scenario: Add AI-suggested knowledge point
- **WHEN** user selects an AI-suggested knowledge point AND clicks "Add to Course"
- **THEN** system creates new knowledge point record with AI-provided title and content

#### Scenario: Search error handling
- **WHEN** AI search API returns error or timeout
- **THEN** system shows error message "Search failed. Please check network connection and try again."

---

### Requirement: Course Deletion
The system SHALL allow users to delete their own courses with confirmation dialog.

#### Scenario: Delete user course
- **WHEN** user clicks "Delete Course" AND confirms deletion in dialog
- **THEN** system removes the course and all associated knowledge points and learning sessions

#### Scenario: Cannot delete sample courses
- **WHEN** user attempts to delete a pre-loaded sample course
- **THEN** system shows message "Sample courses cannot be deleted."

---

### Requirement: Data Integrity for Course Management
The system SHALL ensure data integrity when performing course and knowledge point operations.

#### Scenario: Delete course with active learning sessions
- **WHEN** user attempts to delete a course that has incomplete learning sessions
- **THEN** system shows warning "This course has X in-progress learning sessions. They will be permanently deleted." AND requires explicit confirmation

#### Scenario: Prevent duplicate knowledge point titles
- **WHEN** user adds a knowledge point with title that already exists in the same course
- **THEN** system shows warning "A knowledge point with this title already exists. Continue anyway?" AND allows user to proceed or cancel
