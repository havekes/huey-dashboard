## Context

The Huey Dashboard library currently lacks internal logging. When integrated into a larger FastAPI application, developers have limited visibility into the background processes like signal reception, database operations, WebSocket events, and incoming API requests. To make this library production-ready and easily debuggable, we need to add robust debug logging without forcing a specific logging configuration on the parent application.

## Goals / Non-Goals

**Goals:**
- Provide comprehensive debug-level logging for critical lifecycle events (signals, DB writes, WebSocket broadcasts, API requests).
- Use standard Python `logging` package (`logging.getLogger(__name__)`).
- Ensure the logging respects the parent application's logging configuration (no custom handlers or basicConfig).

**Non-Goals:**
- Implementing custom log formatters or handlers.
- Emitting logs at levels other than `DEBUG` (except where an explicit error is caught, though the scope focuses on debug logging).
- Logging sensitive task arguments (we will log task IDs and statuses, not full payloads, unless generic).

## Decisions

- **Use `logging.getLogger(__name__)`**: This is the standard practice for Python libraries. It allows the parent application to target logs specifically from `huey_dashboard` (e.g., `logging.getLogger("huey_dashboard").setLevel(logging.DEBUG)`).
- **Log Request via API Router Dependency**: Instead of a global middleware which would catch all FastAPI requests in the host app, we will use a dependency injected into our `api_router`. Fastapi dependencies on the APIRouter are an effective way to log requests scoped strictly to the dashboard's endpoints.
- **Log statements placement**:
  - `services/signals.py` -> Log upon signal reception.
  - `services/database.py` -> Log upon successful `upsert_task`.
  - `services/websocket_manager.py` -> Log upon WebSocket `broadcast` and client `connect`/`disconnect`.
  - `api/router.py` -> Add a dependency for logging incoming dashboard API requests.

## Risks / Trade-offs

- **Risk:** High volume of debug logs in a busy Huey worker or dashboard instance.
  - **Mitigation:** All logs will be emitted at the `DEBUG` level. They will be suppressed by default unless the parent app explicitly enables `DEBUG` for the `huey_dashboard` logger.
