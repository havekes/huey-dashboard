## Why

Currently, the Huey Dashboard is structured as a standalone FastAPI application. To increase its utility, it should be reusable as a plugin that can be easily integrated into existing FastAPI applications. This requires a standard initialization function to handle routing and configuration within a host app.

## What Changes

- **NEW**: `init_huey_dashboard` function as the primary entry point for the library.
- **MODIFIED**: Refactor internal dependencies to support dynamic configuration of Huey and Redis connections provided by the host application.
- **NEW**: Customizable router mounting, allowing users to specify the prefix (e.g., `/admin/huey` or `/dashboard`).
- **NEW**: Integration with host app's lifecycle for background polling or signal handling.

## Capabilities

### New Capabilities
- `plugin-initialization`: Provides a single function to attach the dashboard's API and routes to an existing FastAPI instance.
- `external-connection-binding`: Allows the library to use Huey and Redis instances managed by the host application instead of internal defaults.

### Modified Capabilities
- None

## Impact

This change will refactor `src/huey_dashboard/main.py` to move its logic into a reusable initialization function. It affects how the `api_router` and services (like `HueyService` and `WebSocketManager`) are configured, as they must now be scoped to the host app's provided connections.
