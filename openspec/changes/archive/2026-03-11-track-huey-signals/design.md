## Context

Currently, the Huey dashboard tracks task states by periodically polling `huey.pending()` and `huey.scheduled()` and then broadcasting updates via WebSockets. This polling approach is inherently inefficient and misses transitional states (like executing or error) because it only observes the queue at discrete intervals. Huey emits lifecycle signals (`SIGNAL_ENQUEUED`, `SIGNAL_EXECUTING`, etc.) that can be hooked into for real-time tracking.

## Goals / Non-Goals

**Goals:**
- Replace the polling mechanism with event-driven signal handlers.
- Persist task states to a PostgreSQL database.
- Broadcast state changes instantly to connected WebSockets.
- Serve API requests from the database to improve response times.

**Non-Goals:**
- We are not replacing Redis or Huey. This is purely for dashboard tracking.
- We are not managing PostgreSQL server setup; we assume a connection is provided via the plugin initialization.

## Decisions

- **Database**: Use PostgreSQL. The database connection (DSN or pool) will be passed into the `init_huey_dashboard` method. This allows the dashboard to share the host application's database if desired.
- **Concurrency**: Since signal handlers run in Huey consumer processes and the FastAPI app in another, PostgreSQL provides robust, concurrent access to the shared state.
- **WebSocket Broadcast**: The FastApi app will need to be notified when the database changes. We will use Redis Pub/Sub (already available in the tech stack) to publish events from the Huey consumer's signal handler to the FastApi WebSocket manager.

## Risks / Trade-offs

- **[Risk] Connection Management**: If the plugin doesn't correctly handle connection pooling, it might exhaust available PostgreSQL connections.
  → Mitigation: Use a robust connection pool (like `psycopg_pool` or `asyncpg` pools) and ensure the plugin initialization correctly sets this up.
- **[Risk] Cross-Process Event Broadcast**: The Huey consumer runs in a separate process from the FastAPI server. Emitting a WebSocket event directly from the Huey signal handler won't reach the FastAPI WebSocket manager.
  → Mitigation: We will publish a message to a Redis Pub/Sub channel from the signal handler. The FastAPI server will subscribe to this channel and broadcast messages to connected WebSockets.