## Why

Currently, `huey-dashboard` polls the Huey instance for task updates, which is inefficient and less accurate for tracking real-time status changes. Huey provides signals (`SIGNAL_ENQUEUED`, `SIGNAL_EXECUTING`, `SIGNAL_COMPLETE`, `SIGNAL_ERROR`, etc.) that allow for event-driven tracking. By leveraging these signals, we can capture exact task lifecycle events, persist task snapshots to a database, and broadcast these changes efficiently over WebSockets.

## What Changes

- Implement a Huey signal listener to intercept task lifecycle events in real-time.
- Introduce a PostgreSQL database to persistently store task state snapshots, with the connection provided during plugin initialization.
- Update the WebSocket manager to broadcast task events directly from the signal handlers instead of a polling loop.
- Refactor the API to fetch current task state from the PostgreSQL database instead of the Huey queue.
- **BREAKING**: Replaces the periodic polling background task (`poll_huey_updates`) with event-driven signal handlers.

## Capabilities

### New Capabilities
- `task-state-persistence`: Persists task state snapshots into a PostgreSQL database, providing an accurate, queryable source of truth for task statuses.

### Modified Capabilities
- `huey-api`: The API now reads task status from the PostgreSQL database rather than querying Huey's pending and scheduled queues directly.
- `websocket-updates`: WebSocket broadcasts are now triggered by Huey signals instead of a periodic polling loop.

## Impact

- **Code**: Refactoring `HueyService` to use a database; removing `poll_huey_updates` background task; adding a new `DatabaseService` or similar.
- **APIs**: API response times for task lists will improve as they hit a local PostgreSQL DB rather than iterating over Redis queues.
- **Dependencies**: Requires a PostgreSQL driver (e.g., `psycopg` or `asyncpg`), but data storage patterns change.
- **Systems**: Huey workers/consumers will now run the signal handlers, which need access to the database and Redis for broadcasting to WebSockets across processes.