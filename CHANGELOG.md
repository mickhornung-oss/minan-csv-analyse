# Changelog

All notable changes to this project are documented in this file.

## [v1.4.0] - 2026-04-17

### Added

- public documentation architecture with clear public/internal split (`README`, `docs/README`, `docs/internal/*`)
- packaging source isolation under `packaging/pyinstaller/`
- consolidated local quality gate runner: `scripts/quality_gates.py`
- minimal CI baseline in `.github/workflows/ci.yml`
- formal release acceptance checklist: `docs/release_checklist.md`
- release notes file: `docs/release.md`

### Changed

- root and repository framing hardened for public/product presentation
- build pipeline hardened (`build_release.bat`) with fail-fast checks and deterministic cleanup
- packaging/docs alignment fixed for one bundled release sample (`test_csv_deutsch_200x15.csv`)
- status and guidance docs aligned to real build/test/CI behavior

### Verified

- baseline tests green: `pytest -q` (`155 passed` reference run)
- full local quality gate supports compile + tests + build + EXE smoke

### Not Included

- hosted/cloud deployment path
- automated GitHub release artifact publishing
- cross-platform packaging beyond Windows
