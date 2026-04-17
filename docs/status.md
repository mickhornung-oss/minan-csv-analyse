# Project Status

Last updated: 2026-04-17

## Current Position

- Product line: `MinAn 1.4`
- Release identity: `v1.4.0`
- Core app: local CSV analysis desktop tool
- Codebase status: stable for current scope
- Test baseline: green (`pytest -q`)

## Scope Boundaries (Current)

Included:

- local CSV analysis and active-view workflow
- CSV and HTML export
- portable Windows release packaging via PyInstaller
- baseline CI quality checks (Windows)

Not included:

- hosted web demo or cloud deployment
- automated GitHub artifact publishing/release upload
- advanced analytics beyond current profile/quality/chart workflow

## Packaging and Release State

- Build entrypoint: `build_release.bat`
- Build source files: `packaging/pyinstaller/*`
- Release artifact: `dist/MinAn_1_4/`
- Release start path: `dist/MinAn_1_4/MinAn.exe`
- Bundled sample dataset in release: `_internal/sample_data/test_csv_deutsch_200x15.csv`
- Generated artifacts (`build/`, `dist/`, `output/`) are intentionally excluded from version control

## Quality Gate State

- Local baseline gate: `python scripts/quality_gates.py`
- Local full gate: `python scripts/quality_gates.py --with-build --with-exe-smoke`
- CI baseline: `.github/workflows/ci.yml` runs compile + tests on Windows for push/PR
- CI packaging smoke: same workflow, manual dispatch path for build + EXE smoke

## Release Governance State

- Release acceptance checklist: [`release_checklist.md`](release_checklist.md)
- Release notes: [`release.md`](release.md)
- Change history: `../CHANGELOG.md`
- License model: MIT (`../LICENSE`)

## Release Readiness Interpretation

`v1.4.0` is technically releasable for local Windows usage and portfolio/public repository review.
