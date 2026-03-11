## Why

This change replaces `pyright` with `ty`, the new high-performance Python type checker from Astral.
`ty` provides significantly faster type checking (up to 100x faster than `pyright`), better diagnostics, and tighter integration with other Astral tools like `ruff` and `uv` which are already used in this project. Replacing `pyright` will reduce CI times and improve the local developer experience with near-instant feedback.

## What Changes

- **REMOVE**: `pyright` from dev dependencies.
- **ADD**: `ty` to dev dependencies.
- **MODIFY**: Replace `pyright` configuration in `pyproject.toml` with `ty` configuration.
- **MODIFY**: Update CI/CD pipelines and local scripts to use `ty check` instead of `pyright`.
- **MODIFY**: Documentation to reflect the change in toolchain.

## Capabilities

### New Capabilities
- `static-analysis`: Implementation of project-wide static type checking using `ty`.

### Modified Capabilities
- (None)

## Impact

- **Developer Workflow**: Developers will now use `ty check` for local type validation.
- **CI/CD**: The type checking step in `.github/workflows/ci.yml` (and any other automation) will be updated.
- **Performance**: Expect significant reduction in type checking duration.
- **Configuration**: `[tool.pyright]` section in `pyproject.toml` will be replaced by `[tool.ty]`.
