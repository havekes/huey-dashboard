## Why

The Huey Dashboard currently operates silently, making it difficult for parent applications and developers to introspect its internal state and troubleshoot issues. Since this is a library intended to be embedded within larger FastAPI applications, providing detailed, structured debug logs is essential for operational visibility without interfering with the host application's own logging configuration.

## What Changes

- Introduce standard Python `logging` using package-level loggers (`logging.getLogger(__name__)`).
- Emit debug logs when a Huey signal is received.
- Emit debug logs when a task is saved to the database.
- Emit debug logs when an event is broadcasted via WebSockets.
- Emit debug logs when an API request is received by the dashboard.
- The library will not configure any log handlers or formatters, delegating all configuration to the parent project as per best practices.

## Capabilities

### New Capabilities
- `debug-logging`: Defines the logging strategy and specific instrumentation points across the library.

### Modified Capabilities


## Impact

- `src/huey_dashboard/services/signals.py`
- `src/huey_dashboard/services/database.py`
- `src/huey_dashboard/services/websocket_manager.py`
- `src/huey_dashboard/api/router.py` (or dependency injection points)
