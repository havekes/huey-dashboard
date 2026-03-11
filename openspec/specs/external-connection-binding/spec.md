# external-connection-binding Specification

## Purpose
TBD - created by archiving change fastapi-plugin-init. Update Purpose after archive.
## Requirements
### Requirement: Connection Parameters
The `init_huey_dashboard` function SHALL accept a `Huey` instance and an optional Redis connection instance as parameters.

#### Scenario: Injecting Connections
- **WHEN** `init_huey_dashboard(app, huey=host_huey, redis=host_redis, ...)` is called
- **THEN** the library's internal services use `host_huey` and `host_redis` for all Huey operations and background polling.

### Requirement: Signal Binding
The `init_huey_dashboard` function SHALL accept an optional `bind_signals: bool` parameter to enable automatic event capturing via Huey's signal handlers.

#### Scenario: Signal Capture
- **WHEN** `init_huey_dashboard(..., bind_signals=True)` is called and a task is queued in the host's Huey instance
- **THEN** the Huey Dashboard captures the event and broadcasts it via WebSocket.

