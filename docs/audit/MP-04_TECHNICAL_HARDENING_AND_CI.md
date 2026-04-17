# MP-04 - Technical Hardening and CI Baseline

Date: 2026-04-17
Block: 4/5
Status: completed

## 1) Objective

Harden technical reproducibility and establish a minimal, credible CI baseline without introducing feature or architecture churn.

## 2) Implemented hardening

### A) Consolidated quality gate runner

Added `scripts/quality_gates.py`.

Gate chain:

1. compile check (`python -m compileall -q src tests`)
2. automated tests (`python -m pytest -q`)
3. optional release build (`build_release.bat`)
4. optional EXE launch smoke (`dist/MinAn_1_4/MinAn.exe` liveness check)

Supported modes:

- baseline: `python scripts/quality_gates.py`
- full local release validation: `python scripts/quality_gates.py --with-build --with-exe-smoke`

### B) CI baseline introduced

Added `.github/workflows/ci.yml` with two jobs:

- `quality-gates` (push/PR/manual):
  - windows runner
  - python setup
  - dependency install
  - baseline gates (`scripts/quality_gates.py`)

- `packaging-smoke` (manual only):
  - runs full gates including build + EXE smoke

This keeps PR CI stable and lightweight while still enabling reproducible packaging verification on demand.

### C) Reproducibility path tightened in docs

Updated docs to reflect executable quality-chain reality:

- `README.md`
- `docs/development.md`
- `docs/testing.md`
- `docs/packaging.md`
- `docs/status.md`
- `docs/README.md`

All now reference the same gate commands and CI scope.

## 3) Real validation executed

Executed in this workspace:

- `python scripts/quality_gates.py` -> pass
- `python scripts/quality_gates.py --with-build --with-exe-smoke` -> pass

Observed:

- tests stayed green (`155 passed`)
- release build completed
- EXE started and stayed alive during smoke interval

## 4) Quality gates after MP-04

Local baseline gate:

- `python scripts/quality_gates.py`

Local full release gate:

- `python scripts/quality_gates.py --with-build --with-exe-smoke`

CI baseline gate:

- `.github/workflows/ci.yml` / `quality-gates`

Manual CI packaging gate:

- `.github/workflows/ci.yml` / `packaging-smoke`

## 5) Open items (intentionally not in scope)

- license finalization
- signed binaries/notarization
- release publishing automation
- multi-platform CI matrix

These are finalization/governance concerns reserved for the last block.
