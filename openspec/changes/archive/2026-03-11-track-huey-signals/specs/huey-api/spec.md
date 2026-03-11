## MODIFIED Requirements

### Requirement: Task Listing Endpoint
The system SHALL provide a REST endpoint to list all tracked Huey tasks, including historically completed or failed tasks stored in the database.

#### Scenario: Retrieve task list
- **WHEN** a client sends a GET request to the tasks endpoint
- **THEN** the system returns a JSON list of all tasks tracked in the database with their current status and metadata
