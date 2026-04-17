# Release Notes - v1.4.0

Release date: 2026-04-17  
Release scope: local Windows desktop mini-tool

## What This Release Is

`v1.4.0` is the first fully consolidated public repository baseline after repository cleanup, documentation consolidation, packaging hardening, and technical quality-gate/CI baseline work.

## Included

- stable local CSV analysis desktop workflow
- active-view filtering/editing and CSV/HTML export
- reproducible Windows packaging entrypoint (`build_release.bat`)
- portable release layout at `dist/MinAn_1_4/`
- consolidated quality gates via `python scripts/quality_gates.py`
- minimal CI baseline in `.github/workflows/ci.yml`

## Explicitly Not Included

- hosted web deployment/demo
- automated GitHub release artifact publishing
- cross-platform packaging target (non-Windows)

## Release Build Output

Primary executable:

- `dist/MinAn_1_4/MinAn.exe`

Required runtime contents:

- `_internal/sample_data/test_csv_deutsch_200x15.csv`
- `output/reports/`
- `output/csv/`
- `README.md`
- `README_Kurzstart.txt`

## Validation Reference (local)

- baseline quality gates: `python scripts/quality_gates.py`
- full packaging + smoke gate: `python scripts/quality_gates.py --with-build --with-exe-smoke`

See [`release_checklist.md`](release_checklist.md) for the formal acceptance gate.
