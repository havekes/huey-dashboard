# static-analysis Specification

## Purpose
TBD - created by archiving change use-ty-for-type-checking. Update Purpose after archive.
## Requirements
### Requirement: Ty-based Static Analysis
The project SHALL use `ty` as its primary static type checking tool, replacing `pyright`.

#### Scenario: Running type checks locally
- **WHEN** a developer runs `uvx ty check` in the project root
- **THEN** `ty` performs type checking on the `src` directory and reports any type errors or warnings

#### Scenario: CI/CD type checking
- **WHEN** a pull request is created or code is pushed to the main branch
- **THEN** the CI pipeline runs `ty check` and fails if any type errors are detected

### Requirement: Ty Configuration
The project SHALL be configured to use `ty` with settings equivalent to the previous `pyright` setup.

#### Scenario: Configuration in pyproject.toml
- **WHEN** `ty` is executed
- **THEN** it respects the configuration defined in the `[tool.ty]` section of `pyproject.toml`, including source directories and strictness levels

