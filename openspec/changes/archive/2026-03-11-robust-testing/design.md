## Context

The Huey dashboard requires a robust and comprehensive test suite to ensure regressions aren't introduced as the codebase scales. Currently, testing only covers the `ENQUEUED` signal and basic plugin initialization. The system uses a dual-layer approach for data (Database for primary storage, fallback to legacy Huey queue if not configured) and cross-process messaging (Redis Pub/Sub) for real-time WebSocket updates. Testing these specific architectures is crucial.

## Goals / Non-Goals

**Goals:**
- Provide full unit test coverage for `list_tasks` and `get_task` endpoints, including database fallbacks.
- Test all Huey signals (`EXECUTING`, `FINISHED`, `ERROR`, `CANCELED`, `REVOKED`, `RETRYING`, `INTERRUPTED`) and their side-effects (DB insert, Redis publish).
- Test WebSocket connection management, message broadcasting, and Redis Pub/Sub listener behavior.
- Validate failure modes: Redis connection errors, malformed Pub/Sub messages, missing tasks (404s).

**Non-Goals:**
- Refactoring the core architecture of the plugin or services.
- E2E browser testing (testing remains at the integration/unit level via FastAPI's `TestClient` and `pytest`).

## Decisions

- **Test Fixture Strategy**: We will use `unittest.mock.MagicMock` heavily to mock `RedisHuey`, the database connection, and the `redis.asyncio.Redis` instance, ensuring tests are fast and don't require external running services like Redis or a SQL database during the unit test phase.
- **WebSocket Testing**: FastApi's `TestClient.websocket_connect` will be used to simulate client connections. We will mock the `WebSocketManager.broadcast` to verify the pub/sub listener works correctly.
- **Signal Coverage**: Instead of manually triggering Huey events in an actual Huey worker, we will directly call the registered signal handlers with mocked `Task` objects to verify internal state modifications.

## Risks / Trade-offs

- **[Risk] Mocking conceals real-world integration issues** → **Mitigation**: Our mocks will strictly adhere to the interfaces of the real libraries (e.g., using `spec=RedisHuey`). If needed, we will introduce a separate integration test suite in the future, but unit/mocked tests are the priority now to cover all logical edge cases.
