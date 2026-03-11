## ADDED Requirements

### Requirement: Signal Handler Test Coverage
The system SHALL have automated tests verifying the behavior of all registered Huey signal handlers.

#### Scenario: Testing all signal types
- **WHEN** any supported Huey signal is emitted (e.g., executing, finished, error)
- **THEN** tests MUST verify that the task database is updated correctly and a message is published to Redis.

### Requirement: Database Fallback Test Coverage
The system SHALL have automated tests verifying the API's behavior when the database dependency is unavailable.

#### Scenario: Testing fallback to Huey queue
- **WHEN** the API is queried without a database connection configured
- **THEN** tests MUST verify that tasks are fetched directly from the legacy Huey `pending` and `scheduled` queues.

### Requirement: Pub/Sub Listener Resiliency Testing
The system SHALL have automated tests verifying the robustness of the background Redis Pub/Sub listener.

#### Scenario: Testing malformed messages
- **WHEN** the Redis Pub/Sub listener receives a malformed JSON payload
- **THEN** tests MUST verify that the listener does not crash and continues processing subsequent messages.
