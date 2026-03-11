## ADDED Requirements

### Requirement: Task PostgreSQL Storage
The system SHALL persist task state snapshots to a PostgreSQL database whenever a Huey lifecycle signal is emitted.

#### Scenario: Task is enqueued
- **WHEN** a task emits the `SIGNAL_ENQUEUED` event
- **THEN** the system creates or updates a record for that task in the PostgreSQL database with status "enqueued"

#### Scenario: Task fails
- **WHEN** a task emits the `SIGNAL_ERROR` event
- **THEN** the system updates the corresponding task record in the PostgreSQL database with status "error" and records the error details
