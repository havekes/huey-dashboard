## 1. Project Initialization & Dependency Migration

- [x] 1.1 Initialize `uv` project with `uv init`
- [x] 1.2 Migrate existing dependencies from `requirements.txt` to `pyproject.toml` using `uv add -r requirements.txt`
- [x] 1.3 Verify project can be built and run using `uv run`

## 2. Tool Configuration

- [x] 2.1 Configure `ruff` in `pyproject.toml` (linting and formatting)
- [x] 2.2 Configure `pyright` in `pyproject.toml` (type checking)
- [x] 2.3 Configure `pytest` in `pyproject.toml` (testing)

## 3. GitHub Actions Configuration

- [x] 3.1 Create `.github/workflows/ci.yml` for automated quality checks
- [x] 3.2 Implement `lint-type-test` job using `astral-sh/setup-uv`
- [x] 3.3 Verify GitHub Actions workflow configuration

## 4. Verification & Cleanup

- [x] 4.1 Run `uv run ruff check .` and fix or ignore initial violations
- [x] 4.2 Run `uv run pyright` and fix or ignore initial violations
- [x] 4.3 Run `uv run pytest` and ensure all tests pass
- [x] 4.4 Update README with new development workflow instructions
