# huey-dashboard
A monitoring dashboard for Huey tasks.

## Installation

```bash
pip install huey-dashboard
```

## Basic Usage

### 1. Initialize the Dashboard in your FastAPI app

```python
from fastapi import FastAPI
from huey_dashboard import init_huey_dashboard
from my_app.tasks import huey  # Your Huey instance

app = FastAPI()

init_huey_dashboard(
    app,
    huey,
    db_url="postgresql+asyncpg://user:pass@localhost/mydb",
    redis_url="redis://localhost:6379/0",  # Optional, for real-time updates
)
```

### 2. Initialize Worker Signals

In the module where your Huey instance is defined:

```python
from huey import RedisHuey
from huey_dashboard import init_worker_signals

huey = RedisHuey("my-app", url="redis://localhost:6379/0")

init_worker_signals(
    huey,
    db_url="postgresql+asyncpg://user:pass@localhost/mydb",
    redis_url="redis://localhost:6379/0",
)
```

---

## How to contribute

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
