## Why

The current test suite covers basic initialization and enqueueing but lacks comprehensive coverage for edge cases, error states, and real-time interactions. To ensure the reliability of the Huey dashboard, we must implement a robust test suite that validates all Huey events, Redis connection states, API endpoints, and WebSocket message broadcasting, preventing regressions in production.

## What Changes

- Add comprehensive tests for all Huey task signals (`EXECUTING`, `FINISHED`, `ERROR`, `CANCELED`, `REVOKED`, `RETRYING`, `INTERRUPTED`).
- Add tests for Redis `publish` failure scenarios during signal handling.
- Add tests for `WebSocketManager`'s Redis Pub/Sub listener, including handling malformed JSON and abrupt connection drops.
- Add exhaustive endpoint tests for `/tasks/` and `/tasks/{task_id}`, including 404 handling and database fallback behavior.
- Add WebSocket endpoint tests to verify connection lifecycle and `WebSocketManager.broadcast` behavior with disconnected clients.

## Capabilities

### New Capabilities
- `test-coverage`: Comprehensive testing capability that formally defines the requirements and boundaries for all integration and unit tests covering signals, endpoints, and real-time events.

### Modified Capabilities
- `huey-api`: Adding formal requirements for fallback legacy behavior.
- `websocket-updates`: Adding formal requirements for error handling and connection drops.

## Impact

- `tests/test_signals.py`, `tests/test_plugin.py`, and new test files (`test_endpoints.py`, `test_websockets.py`).
- Increased overall codebase confidence and strict verification of all edge cases.
