# plugin-initialization Specification

## Purpose
TBD - created by archiving change fastapi-plugin-init. Update Purpose after archive.
## Requirements
### Requirement: Library Export
The library SHALL export an `init_huey_dashboard` function as its primary entry point for integration.

#### Scenario: Basic Function Check
- **WHEN** the library is imported from the root package
- **THEN** the `init_huey_dashboard` function is available.

### Requirement: Application Attachment
The `init_huey_dashboard` function SHALL accept a `FastAPI` application instance as its first argument and mount the library's API router onto it.

#### Scenario: Default Mounting
- **WHEN** `init_huey_dashboard(app, ...)` is called without a custom prefix
- **THEN** the Huey Dashboard router is included in the host app at the default `/huey` path.

### Requirement: Customizable Path
The `init_huey_dashboard` function SHALL accept an optional `api_prefix` parameter to specify the base path for the dashboard's API.

#### Scenario: Custom Path Mounting
- **WHEN** `init_huey_dashboard(app, api_prefix="/admin/huey", ...)` is called
- **THEN** the Huey Dashboard router is included in the host app at `/admin/huey`.

