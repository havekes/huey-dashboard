## 1. Database & Plugin Integration

- [x] 1.1 Create `src/huey_dashboard/services/database.py` to manage the PostgreSQL connection/pool and define `tasks` table schema (id, name, status, args, kwargs, result, error, timestamp).
- [x] 1.2 Implement repository methods in `database.py` for task state updates (`upsert_task`, `get_all_tasks`, `get_task`).
- [x] 1.3 Update `init_huey_dashboard` (or its equivalent in the core setup) to accept a PostgreSQL connection or pool as a parameter and pass it to the services.
- [x] 1.4 Add necessary PostgreSQL drivers (e.g., `psycopg` or `asyncpg`) to `pyproject.toml`.

## 2. Cross-Process Event Broadcast

- [x] 2.1 Refactor `src/huey_dashboard/services/websocket_manager.py` to support Redis Pub/Sub listener for incoming events.
- [x] 2.2 Update the plugin initialization logic to start a background task that listens on the Redis Pub/Sub channel and routes to `WebSocketManager.broadcast`.

## 3. Signal Handlers

- [x] 3.1 Create `src/huey_dashboard/services/signals.py` to register `@huey.signal()` listeners for all relevant task lifecycle events.
- [x] 3.2 Update signal handlers to persist task state snapshots to the PostgreSQL database via `database.py`.
- [x] 3.3 Update signal handlers to publish real-time state change events to the Redis Pub/Sub channel.
- [x] 3.4 Ensure the signal handlers are properly imported and bound when the dashboard plugin is initialized (conditionally via settings if needed).

## 4. API & Polling Refactor

- [x] 4.1 Refactor `HueyService.list_tasks` to read the task list from the PostgreSQL database instead of querying `huey.pending()`/`huey.scheduled()`.
- [x] 4.2 Refactor `HueyService.get_task_details` to read from the PostgreSQL database.
- [x] 4.3 Remove the deprecated `poll_huey_updates` background polling task entirely.

## 5. Testing

- [x] 5.1 Add unit tests for the PostgreSQL `database.py` operations (using a test DB or mock).
- [x] 5.2 Add unit tests for the Huey signal handlers to ensure database updates and Redis Pub/Sub publishes occur correctly.
- [x] 5.3 Validate the complete pipeline with updated tests for the refactored API and WebSocket endpoints.
