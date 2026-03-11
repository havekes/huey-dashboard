# huey-dashboard
A monitoring dashboard for Huey tasks

## Development Workflow

This project uses `uv` for dependency management and environment isolation.

### Prerequisites

- [uv](https://github.com/astral-sh/uv)

### Setup

```bash
uv sync
```

### Quality Checks

#### Linting & Formatting

```bash
uv run ruff check .
uv run ruff format .
```

#### Type Checking

```bash
uv run ty check
```

#### Testing

```bash
uv run pytest
```
