## Context

The project currently uses `pyright` for static type checking. While effective, `pyright` can be slower in CI/CD and large local development environments. Astral's new `ty` tool offers significantly improved performance and tighter integration with existing Astral-based tooling (`ruff`, `uv`).

## Goals / Non-Goals

**Goals:**
- Replace `pyright` with `ty` as the project-wide type checking tool.
- Maintain at least the same level of type safety and error reporting.
- Improve performance for type checking steps in CI/CD and local development.
- Consolidate toolchain configuration in `pyproject.toml`.

**Non-Goals:**
- Fix any pre-existing type errors discovered by `ty` (unless they are trivial or block the transition).
- Transition away from `ruff` or `pytest`.

## Decisions

- **Use `[tool.ty]` in `pyproject.toml`**: This centralizes configuration. We will map current `pyright` settings to their `ty` equivalents.
- **Update CI to use `uv run ty check`**: This replaces the `uv run pyright` step in `.github/workflows/ci.yml`.
- **Remove `pyright` from `dev` dependencies**: This reduces environment footprint and prevents confusion.

## Risks / Trade-offs

- **[Risk] `ty` is in beta** → **Mitigation**: We will monitor stability and keep the transition reversible if critical issues arise. However, since the user explicitly requested it, we proceed.
- **[Risk] Behavioral Differences** → **Mitigation**: Some type errors may be reported differently. We will perform a baseline check and address significant discrepancies.
