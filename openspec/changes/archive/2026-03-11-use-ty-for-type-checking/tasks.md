## 1. Dependency Management

- [x] 1.1 Remove `pyright` from `dev` dependencies using `uv remove --dev pyright`
- [x] 1.2 Add `ty` to `dev` dependencies using `uv add --dev ty`

## 2. Configuration

- [x] 2.1 Remove `[tool.pyright]` configuration from `pyproject.toml`
- [x] 2.2 Add `[tool.ty]` configuration to `pyproject.toml` with equivalent settings (include `src`, set type checking mode, target Python version)

## 3. CI/CD Integration

- [x] 3.1 Update `.github/workflows/ci.yml` to replace the `Run pyright` step with `Run ty check`

## 4. Verification

- [x] 4.1 Run `uv run ty check` locally to verify configuration and type safety
- [x] 4.2 Fix any trivial type errors reported by `ty` to ensure a clean baseline (if necessary)
