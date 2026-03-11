## Why

A dashboard is needed to monitor and manage Redis Huey tasks, but currently, there is no standardized API layer to interface with Huey. This change initializes a new Python library to provide a robust, asynchronous FastAPI backend that will serve as the foundation for the future dashboard, enabling real-time task updates via WebSockets.

## What Changes

- Initialize a new Python project structure optimized for a FastAPI web application.
- Setup FastAPI with asynchronous endpoints for interacting with Redis Huey.
- Implement WebSocket infrastructure for broadcasting live task status updates.
- Establish architectural patterns following industry best practices: separation of concerns, dependency injection, and asynchronous methods.

## Capabilities

### New Capabilities
- `huey-api`: Core FastAPI application and REST endpoints for querying and managing Huey tasks.
- `websocket-updates`: WebSocket connections and broadcasting logic for real-time task status updates.

### Modified Capabilities
- (None)

## Impact

- Introduces a new standalone Python project/library.
- Adds new dependencies including FastAPI, Uvicorn, Redis, and WebSockets.
- Establishes the architectural foundation for all future API development related to the Huey dashboard.