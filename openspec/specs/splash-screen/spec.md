## ADDED Requirements

### Requirement: Show brand splash screen on app launch
The system SHALL display a brand splash screen when the app launches, consisting of the app logo, app name, and tagline.

#### Scenario: Splash screen displays logo
- **WHEN** the app is launched
- **THEN** the splash screen SHALL display the brand logo (foreground.png) centered at the top of the loading area

#### Scenario: Splash screen displays app name
- **WHEN** the splash screen is shown
- **THEN** the app name "问枢" SHALL be displayed below the logo

#### Scenario: Splash screen displays tagline
- **WHEN** the splash screen is shown
- **THEN** the tagline "是什么 → 为什么 → 怎么用" SHALL be displayed below the app name

### Requirement: Preload necessary data on splash screen
The system SHALL preload required data in the background while the splash screen is visible.

#### Scenario: Database initialization
- **WHEN** the splash screen appears
- **THEN** the system SHALL initialize the local database (study_machine.db) before proceeding

#### Scenario: Sample course loading
- **WHEN** the database is initialized
- **THEN** the system SHALL load sample courses if they have not been loaded before

#### Scenario: Onboarding check
- **WHEN** sample courses are loaded
- **THEN** the system SHALL check if the user has completed onboarding

### Requirement: Navigate after loading completes
The system SHALL automatically navigate to the appropriate page after all data is preloaded.

#### Scenario: First-time user navigates to onboarding
- **WHEN** loading completes and the user has not completed onboarding
- **THEN** the system SHALL show the onboarding overlay instead of navigating away

#### Scenario: Returning user navigates to home
- **WHEN** loading completes and the user has already completed onboarding
- **THEN** the system SHALL navigate to the HomePage via replaceUrl

### Requirement: Handle loading errors gracefully
The system SHALL display an error state if data loading fails.

#### Scenario: Error state on initialization failure
- **WHEN** database initialization or data loading fails
- **THEN** the system SHALL display an error message with a retry button

#### Scenario: Retry after error
- **WHEN** the user clicks the retry button on the error screen
- **THEN** the system SHALL restart the initialization process

### Requirement: Show loading indicator while initializing
The system SHALL display a loading progress indicator while data is being loaded.

#### Scenario: Loading spinner visible during init
- **WHEN** data is being initialized
- **THEN** a LoadingProgress indicator SHALL be visible below the app info
