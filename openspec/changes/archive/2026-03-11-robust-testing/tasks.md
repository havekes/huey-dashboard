## 1. Signal Handler Tests

- [x] 1.1 Expand `test_signals.py` to cover `EXECUTING`, `FINISHED`, and `ERROR` signals, verifying DB upsert and Redis publish.
- [x] 1.2 Expand `test_signals.py` to cover `CANCELED`, `REVOKED`, `RETRYING`, and `INTERRUPTED` signals.
- [x] 1.3 Add test in `test_signals.py` for Redis publish failure (e.g., connection error) during signal processing, ensuring graceful handling.

## 2. API Endpoint Tests

- [x] 2.1 Create `tests/test_endpoints.py` and test `list_tasks` with mocked database tasks.
- [x] 2.2 Test `get_task` endpoint in `test_endpoints.py` for successful retrieval and 404 response when not found.
- [x] 2.3 Test endpoint fallback behavior in `test_endpoints.py` when database dependency is not available (mock Huey `pending` and `scheduled` queues).

## 3. WebSocket and Pub/Sub Tests

- [x] 3.1 Create `tests/test_websockets.py` and test successful WebSocket connection, message receipt, and disconnection logic.
- [x] 3.2 Add test in `test_websockets.py` for `WebSocketManager.broadcast` to handle client disconnection exceptions gracefully without crashing.
- [x] 3.3 Add test in `test_websockets.py` for the Redis Pub/Sub listener (`_listen_to_pubsub`), verifying correct broadcast on message receipt.
- [x] 3.4 Add test for Pub/Sub listener receiving malformed JSON payloads, ensuring it doesn't crash the listener loop.