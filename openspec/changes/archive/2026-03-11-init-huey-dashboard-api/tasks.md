## 1. Project Setup

- [x] 1.1 Create core Python project structure and files (e.g., `main.py`, `routers/`, `services/`, `core/`)
- [x] 1.2 Setup requirements or environment configuration for dependencies (fastapi, uvicorn, websockets, redis, huey)

## 2. Core Architecture & Configuration

- [x] 2.1 Implement configuration management (e.g., loading environment variables for Redis/Huey connections)
- [x] 2.2 Set up dependency injection providers for Redis and Huey clients in the `core/` or `dependencies/` module
- [x] 2.3 Initialize the FastAPI application and register global exception handlers

## 3. Huey API Endpoints

- [x] 3.1 Implement the service layer (`services/huey_service.py`) for querying the Huey queue and task states
- [x] 3.2 Create the REST endpoint (`GET /tasks`) to list currently queued and active Huey tasks
- [x] 3.3 Create the REST endpoint (`GET /tasks/{task_id}`) to fetch detailed information about a specific task by its ID

## 4. WebSocket Updates

- [x] 4.1 Implement a WebSocket connection manager (`services/websocket_manager.py`) to handle active connections and broadcasting
- [x] 4.2 Create the WebSocket endpoint (`WS /updates`) to accept client connections and register them with the manager
- [x] 4.3 Implement an event listener or polling mechanism that monitors Huey task state changes and triggers broadcasts to all connected WebSocket clients