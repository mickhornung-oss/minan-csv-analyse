# Testing

## Baseline Quality Gates

```bash
python scripts/quality_gates.py
```

This executes:

- compile check (`compileall`) on `src/` and `tests/`
- full `pytest -q`

## Full Local Technical Gates

```bash
python scripts/quality_gates.py --with-build --with-exe-smoke
```

Additional gates:

- release build via `build_release.bat`
- executable liveness smoke check

Reference test run in this workspace on 2026-04-17:

- `155 passed`

## Main Test Areas

- CSV import behavior and detection logic
- Dataset profile and quality services
- Transform/edit behavior
- CSV export and HTML report generation
- Runtime path logic and safety constraints
- GUI smoke path (`tests/test_product_smoke_gui.py`)

## Targeted Smoke Validation Command

You can run only the GUI smoke path if needed:

```bash
pytest -q tests/test_product_smoke_gui.py
```

## Expected Outcome

A green test run is required before packaging/release validation.
