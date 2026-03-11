## MODIFIED Requirements

### Requirement: Real-time Task Status Broadcast
The system SHALL broadcast task status changes (e.g., queued, started, finished, failed) to all connected WebSocket clients in real-time, driven by direct signal handlers rather than periodic polling.

#### Scenario: Task status changes to finished
- **WHEN** a Huey task completes its execution
- **THEN** the system immediately broadcasts a "task finished" JSON payload with the task ID to all connected WebSocket clients via a cross-process messaging system (e.g., Redis Pub/Sub)
