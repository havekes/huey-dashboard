## Context

The Huey Dashboard is currently a standalone FastAPI application. To allow integration into other projects, it must be refactored into a library. This change introduces an initialization function that configures the dashboard's routes, dependencies, and event handlers within a host application's context.

## Goals / Non-Goals

**Goals:**
- Provide a clean, single-function entry point for integration.
- Enable dynamic configuration of Huey and Redis connections.
- Support customizable URL prefixing for the dashboard API.
- Support Huey's signal-based event capturing as an alternative or supplement to polling.

**Non-Goals:**
- Removing the existing standalone entry point (it will be refactored to use the new `init` function).
- Support for multiple Huey instances within a single dashboard instance (for now).

## Decisions

### 1. State Management via `app.state`
**Decision:** Store the Huey client and Redis connection on `app.state.huey_dashboard`.
**Rationale:** This avoids global variables and ensures the dashboard's state is scoped to the host FastAPI instance.
**Alternatives:** 
- *Global variables:* Poor for testing and multiple app instances.
- *FastAPI Dependencies:* Hard to configure dynamically after the app is created without using `app.state`.

### 2. Dependency Injection Refactoring
**Decision:** Refactor `get_huey_client` and other dependency providers to read from `request.app.state.huey_dashboard`.
**Rationale:** Ensures all routes correctly access the connections provided during initialization.

### 3. Huey Signals Integration
**Decision:** Use Huey's signal decorators (`@huey.signal()`) to capture task events if `bind_signals=True`.
**Rationale:** Provides real-time updates without the overhead of polling. Polling will remain as a fallback if signals are not supported or configured.

### 4. Router Mounting
**Decision:** Use `app.include_router(api_router, prefix=api_prefix)`.
**Rationale:** Standard FastAPI pattern for mounting sub-applications or routers.

## Risks / Trade-offs

- **[Risk] Host Lifecycle Conflicts** → The library needs to run a background task for polling. If the host has its own lifespan, it might not know how to handle the library's task. **Mitigation:** Provide a utility to wrap lifespans or use `app.add_event_handler` (deprecated in 0.90.0 but still works) or documented manual integration steps.
- **[Risk] Performance Overhead** → Polling can be heavy on large Huey instances. **Mitigation:** Default polling interval is conservative (5s), and signal binding is encouraged for real-time updates.
