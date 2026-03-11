## ADDED Requirements

### Requirement: WebSocket Connection
The system SHALL accept WebSocket connections from clients for the purpose of streaming task updates.

#### Scenario: Successful WebSocket connection
- **WHEN** a client initiates a WebSocket connection to the designated updates endpoint
- **THEN** the connection is accepted and kept alive

### Requirement: Real-time Task Status Broadcast
The system SHALL broadcast task status changes (e.g., queued, started, finished, failed) to all connected WebSocket clients.

#### Scenario: Task status changes to finished
- **WHEN** a Huey task completes its execution
- **THEN** the system broadcasts a "task finished" JSON payload with the task ID to all connected WebSocket clients