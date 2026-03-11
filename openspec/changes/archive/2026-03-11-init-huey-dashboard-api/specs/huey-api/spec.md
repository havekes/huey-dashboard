## ADDED Requirements

### Requirement: Task Listing Endpoint
The system SHALL provide a REST endpoint to list currently queued and active Huey tasks.

#### Scenario: Retrieve task list
- **WHEN** a client sends a GET request to the tasks endpoint
- **THEN** the system returns a JSON list of tasks with their current status and metadata

### Requirement: Task Details Endpoint
The system SHALL provide an endpoint to fetch detailed information about a specific task by its ID.

#### Scenario: Retrieve specific task details
- **WHEN** a client sends a GET request with a valid task ID
- **THEN** the system returns detailed JSON metadata for that specific task

#### Scenario: Retrieve non-existent task details
- **WHEN** a client sends a GET request with an invalid or non-existent task ID
- **THEN** the system returns a 404 Not Found response