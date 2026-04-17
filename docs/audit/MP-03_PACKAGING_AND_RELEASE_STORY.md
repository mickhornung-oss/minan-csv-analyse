# MP-03 - Packaging and Release Story

Date: 2026-04-17
Block: 3/5
Status: completed

## 1) What was unclear before

Before MP-03, packaging had multiple ambiguities:

- `build_release.bat` was interactive (`pause`) and not automation-friendly.
- Build preconditions were not validated early (spec/version/sample presence).
- Sample data policy was inconsistent between docs and actual packaged output.
- Spec root path had changed recently and was error-prone.
- Release documentation did not precisely describe include/exclude behavior.

## 2) Technical decisions made

### Decision A - Single reproducible build entry

- Keep one build entrypoint: `build_release.bat`.
- Script is now fail-fast and non-interactive.
- Script now cleans generated folders before building (`build/` and target release folder).

### Decision B - Explicit packaging source of truth

- Keep packaging sources in `packaging/pyinstaller/`.
- Spec and version metadata remain versioned.

### Decision C - Sample-data policy fixed

- Release includes exactly one bundled sample file:
  `test_csv_deutsch_200x15.csv`
- Spec now packages this file explicitly instead of the whole sample folder.

## 3) Implemented changes

### Build script

`build_release.bat` now:

1. validates PyInstaller availability
2. validates required files exist:
   - `packaging/pyinstaller/minan_v1.spec`
   - `packaging/pyinstaller/windows_version_info.txt`
   - `assets/sample_data/test_csv_deutsch_200x15.csv`
3. cleans old generated build/release dirs
4. builds with `python -m PyInstaller ... --clean --noconfirm`
5. validates `dist/MinAn_1_4/MinAn.exe` exists
6. prepares output folders and copies release readme files
7. exits with proper return code (no pause)

### PyInstaller spec

`packaging/pyinstaller/minan_v1.spec` now:

- validates icon/sample/version file existence at spec-exec time
- packages exactly one sample CSV (`test_csv_deutsch_200x15.csv`)
- uses corrected `PROJECT_ROOT` path resolution from spec directory

### Documentation

Updated:

- `docs/packaging.md`
- `docs/status.md`
- `README.md` (packaging section sample-data line)

Docs now match real build behavior and release contents.

## 4) Final release structure (validated)

Build output root:

- `dist/MinAn_1_4/`

Minimum guaranteed structure:

- `MinAn.exe`
- `_internal/sample_data/test_csv_deutsch_200x15.csv`
- `output/reports/`
- `output/csv/`
- `README_Kurzstart.txt`
- `README.md`

## 5) Reproducible build path (external developer)

From fresh clone:

1. `pip install -r requirements.txt`
2. run `build_release.bat`
3. run `dist/MinAn_1_4/MinAn.exe`

No hidden custom script outside repository required.

## 6) Build + smoke evidence

Executed in this workspace:

- `build_release.bat` -> success
- release folder created under `dist/MinAn_1_4/`
- bundled sample file check -> exactly one file present
- EXE launch smoke:
  - process started
  - process stayed running
  - process was terminated intentionally after verification

## 7) Remaining open items

Not in MP-03 scope:

- CI-based release validation pipeline
- code-signing/notarization strategy
- release artifact publishing workflow
- binary size optimization/dep-pruning in packaged runtime
