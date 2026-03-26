## ADDED Requirements

### Requirement: Debug logging for Huey signals
The system SHALL emit a debug log whenever a Huey signal is received.

#### Scenario: Signal is received
- **WHEN** the `handle_task_event` function is invoked
- **THEN** a debug log is emitted containing the signal type and task ID

### Requirement: Debug logging for task database operations
The system SHALL emit a debug log whenever a task is successfully saved or updated in the database.

#### Scenario: Task is saved
- **WHEN** the `upsert_task` function successfully writes to the database
- **THEN** a debug log is emitted containing the task ID and its new status

### Requirement: Debug logging for WebSocket events
The system SHALL emit a debug log whenever an event is pushed to WebSocket clients.

#### Scenario: Event is broadcasted
- **WHEN** the `broadcast` method is called with a message
- **THEN** a debug log is emitted detailing the broadcast

### Requirement: Debug logging for incoming requests
The system SHALL emit a debug log whenever a request is received by the Huey Dashboard API router.

#### Scenario: API request received
- **WHEN** an HTTP request hits any endpoint under the Huey Dashboard API prefix
- **THEN** a debug log is emitted showing the request method and path
