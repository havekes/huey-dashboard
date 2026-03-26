## 1. Implement Debug Logging in Services

- [x] 1.1 Add `import logging` and `logger = logging.getLogger(__name__)` to `src/huey_dashboard/services/signals.py`.
- [x] 1.2 In `signals.py`, log the received signal and task ID at the debug level inside `handle_task_event`.
- [x] 1.3 Add `import logging` and `logger = logging.getLogger(__name__)` to `src/huey_dashboard/services/database.py`.
- [x] 1.4 In `database.py`, log the task ID and status at the debug level inside `upsert_task` after the query executes.
- [x] 1.5 Add `import logging` and `logger = logging.getLogger(__name__)` to `src/huey_dashboard/services/websocket_manager.py`.
- [x] 1.6 In `websocket_manager.py`, log the broadcasted message at the debug level inside `broadcast`.
- [x] 1.7 In `websocket_manager.py`, log connections and disconnections in `connect` and `disconnect` at the debug level.

## 2. Implement API Request Logging

- [x] 2.1 Add a dependency in `src/huey_dashboard/api/router.py` to log incoming requests at the debug level.
- [x] 2.2 Define the asynchronous dependency function `log_request(request: Request)` that uses `logger.debug` to log `request.method` and `request.url.path`.
- [x] 2.3 Ensure `api_router` is initialized with `dependencies=[Depends(log_request)]`.

## 3. Testing and Validation

- [x] 3.1 Update or add unit tests to verify that logs are emitted when signals are received.
- [x] 3.2 Update or add unit tests to verify that logs are emitted when a task is saved.
- [x] 3.3 Verify that the parent application logging configuration correctly intercepts and formats the dashboard's debug logs.
- [x] 3.4 Run the full test suite (`pytest`) to ensure no regressions were introduced.
