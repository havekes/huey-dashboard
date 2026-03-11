## Context

The `huey-dashboard` project currently uses a standard `requirements.txt` for dependency management. It lacks a unified toolchain for linting, type checking, and automated testing, leading to potential inconsistencies and slower development cycles.

## Goals / Non-Goals

**Goals:**
- Migrate to `uv` for faster and more reliable dependency management.
- Implement a modern, high-performance toolchain (`ruff`, `pyright`, `pytest`).
- Automate all quality checks in GitHub Actions.
- Consolidate tool configuration into `pyproject.toml`.

**Non-Goals:**
- Rewriting existing application code to fix all linting or type errors (the goal is to *enable* the tools).
- Implementing complex deployment pipelines beyond basic CI checks.

## Decisions

- **Dependency Management: `uv` over `pip`/`poetry`**: `uv` is a modern, extremely fast alternative that replaces multiple tools (`pip`, `venv`, `pip-tools`) with a single binary. It offers better performance and a more cohesive developer experience.
- **Linting & Formatting: `ruff` over `flake8`/`black`**: `ruff` is written in Rust and is orders of magnitude faster than Python-based alternatives. It combines linting and formatting into one tool, simplifying configuration.
- **Type Checking: `pyright` over `mypy`**: `pyright` is faster and provides better support for modern Python features and VS Code integration. It's well-suited for high-performance development workflows.
- **Automated Checks: GitHub Actions**: Standardize on GitHub Actions for CI, utilizing `astral-sh/setup-uv` for efficient environment setup in the cloud.

## Risks / Trade-offs

- **Migration complexity**: Some dependencies in `requirements.txt` might require manual adjustment when moving to `pyproject.toml`. → **Mitigation**: Use `uv add -r requirements.txt` to automate the migration as much as possible and verify with a fresh installation.
- **Initial tool noise**: New linting and type checking rules might flag many existing issues. → **Mitigation**: Configure `ruff` and `pyright` with sensible defaults and use `# ruff: noqa` or similar if necessary to allow a gradual cleanup of the codebase.
