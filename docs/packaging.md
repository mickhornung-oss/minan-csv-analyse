# Packaging and Build

Release identity: `v1.4.0`

## Build Entry Point

```bat
build_release.bat
```

The script is fail-fast and performs:

1. precondition checks (PyInstaller, spec, version file, sample CSV)
2. cleanup of previous generated `build/` and target `dist/MinAn_1_4/`
3. fresh PyInstaller build (`--clean --noconfirm`)
4. post-build validation (`MinAn.exe` must exist)
5. release-root preparation (`output/reports`, `output/csv`)
6. copy of user-facing readme files into release root

## Build Source of Truth

PyInstaller input files:

- `packaging/pyinstaller/minan_v1.spec`
- `packaging/pyinstaller/windows_version_info.txt`

Spec entrypoint:

- `src/minan_v1/main.py`

## Build Prerequisites

- Windows 10/11
- Python 3.10+
- install dependencies with `pip install -r requirements.txt`

## Expected Release Layout

```text
dist/MinAn_1_4/
|- MinAn.exe
|- _internal/
|  `- sample_data/
|     `- test_csv_deutsch_200x15.csv
|- output/
|  |- reports/
|  `- csv/
|- README_Kurzstart.txt
`- README.md
```

## Release Start Path

End-user start command:

`dist\\MinAn_1_4\\MinAn.exe`

## Release Include/Exclude Policy

Included in release:

- executable (`MinAn.exe`)
- runtime payload (`_internal/`)
- exactly one bundled sample dataset (`_internal/sample_data/test_csv_deutsch_200x15.csv`)
- output folders (`output/reports`, `output/csv`)
- release readmes

Excluded from release repository tracking:

- `build/` (generated)
- `dist/` (generated)
- `output/` (runtime-generated user data)

## Artifact Policy

- `build/`, `dist/`, and `output/` are generated and excluded from git.
- Packaging source files are versioned under `packaging/pyinstaller/`.

## Packaging Scope

This repository documents Windows portable packaging only.
Cross-platform packaging is currently out of scope.

## Minimal Smoke Validation (after build)

1. Verify `dist/MinAn_1_4/MinAn.exe` exists.
2. Launch executable.
3. Confirm app window opens.
4. Confirm `output/reports` and `output/csv` exist under release root.

For a formal acceptance gate list, use [`release_checklist.md`](release_checklist.md).

For one-command local execution of compile/test/build/smoke gates, use:

`python scripts/quality_gates.py --with-build --with-exe-smoke`
