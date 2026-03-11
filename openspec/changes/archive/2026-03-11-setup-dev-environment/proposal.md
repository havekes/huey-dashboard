## Why

This change modernizes the Python development environment to ensure performance, consistency, type safety, and automated quality checks. By integrating `uv`, `ruff`, `pyright`, and `pytest`, we improve developer efficiency and project reliability.

## What Changes

- **Dev Tools Setup**: Initialize project with `uv` for dependency management and environment isolation.
- **Linting & Formatting**: Configure `ruff` to enforce consistent code style and identify potential issues.
- **Type Checking**: Integrate `pyright` for static type analysis (previously "ty").
- **Testing**: Set up `pytest` as the standard testing framework.
- **CI/CD Pipeline**: Add GitHub Actions configuration for automated linting, type checking, and testing on PRs and merges.

## Capabilities

### New Capabilities
- `dev-tools-setup`: Project management via `uv`, linting via `ruff`, type checking via `pyright`, and testing via `pytest`.
- `ci-cd-pipeline`: Automated workflows for code quality verification in GitHub Actions.

### Modified Capabilities
- (None - no existing specs listed in openspec/specs/ or requirements)

## Impact

- `requirements.txt`: Will be migrated to `pyproject.toml` and managed by `uv`.
- `pyproject.toml`: New configuration file for project metadata and tools.
- `.github/workflows/`: New GitHub Actions workflow files for automated checks.
- Developer workflow: Standardizing on `uv run`, `ruff`, and `pytest`.
