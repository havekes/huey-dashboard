## 1. Core Refactoring (State & Dependencies)

- [x] 1.1 Update `src/huey_dashboard/core/dependencies.py` to lookup Huey and Redis clients from `request.app.state`.
- [x] 1.2 Modify `HueyService` to accept a Huey instance in its constructor instead of relying on globals.
- [x] 1.3 Refactor `WebSocketManager` to be instantiable per application or stored in `app.state`.
- [x] 1.4 Update all endpoints in `src/huey_dashboard/api/endpoints/` to use the new dependency patterns.

## 2. Implementation of Initialization Function

- [x] 2.1 Create `src/huey_dashboard/__init__.py` (or a dedicated module) and export the `init_huey_dashboard` function.
- [x] 2.2 Implement `init_huey_dashboard(app: FastAPI, huey: Huey, redis=None, api_prefix: str = "/huey", bind_signals: bool = False)`.
- [x] 2.3 Add logic to mount the `api_router` with the provided `api_prefix`.
- [x] 2.4 Implement the Huey signal binding logic if `bind_signals` is enabled.

## 3. Background Task & Lifespan Integration

- [x] 3.1 Refactor `poll_huey_updates` to accept the application state and use injected connections.
- [x] 3.2 Update `init_huey_dashboard` to start the background poller using `app.add_event_handler("startup", ...)` or a provided utility.

## 4. Standalone Mode Refactor

- [x] 4.1 Refactor `src/huey_dashboard/main.py` to use `init_huey_dashboard` for its own setup.
- [x] 4.2 Ensure all environment variables are correctly mapped to the `init` function call in standalone mode.

## 5. Verification & Testing

- [x] 5.1 Create a new test suite that simulates a host FastAPI app integrating the dashboard.
- [x] 5.2 Test routing with custom prefixes (e.g., verifying `/custom/api/tasks` works).
- [x] 5.3 Verify that WebSocket updates are correctly broadcast when signals are triggered.
- [x] 5.4 Ensure standalone mode is still fully functional and passes existing tests.
