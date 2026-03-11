# dev-tools-setup Specification

## Purpose
TBD - created by archiving change setup-dev-environment. Update Purpose after archive.
## Requirements
### Requirement: uv project management
The system SHALL use `uv` for project management, including dependency resolution, environment isolation, and project-wide script execution.

#### Scenario: uv initialization
- **WHEN** developer runs `uv init`
- **THEN** project is initialized with a `pyproject.toml` file containing basic project metadata

### Requirement: ruff linting and formatting
The system SHALL use `ruff` to enforce code style and identify common programming errors.

#### Scenario: ruff check
- **WHEN** developer runs `uv run ruff check .`
- **THEN** `ruff` reports all linting violations according to the project's configuration

#### Scenario: ruff formatting
- **WHEN** developer runs `uv run ruff format .`
- **THEN** `ruff` reformats the code to match the project's style guide

### Requirement: pyright type checking
The system SHALL use `pyright` to perform static type analysis on the codebase.

#### Scenario: pyright analysis
- **WHEN** developer runs `uv run pyright`
- **THEN** `pyright` identifies and reports type errors in the codebase

### Requirement: pytest unit testing
The system SHALL use `pytest` as the framework for unit and integration testing.

#### Scenario: run tests
- **WHEN** developer runs `uv run pytest`
- **THEN** `pytest` discovers and executes all tests in the project

