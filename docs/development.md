# Development Setup

## Prerequisites

- Windows 10/11
- Python 3.10+
- `pip`

## Install

```bash
pip install -r requirements.txt
```

## Run Application

```bat
run_dev.bat
```

Equivalent direct command:

```bash
python src/minan_v1/main.py
```

## Useful Paths

- Source: `src/minan_v1/`
- Tests: `tests/`
- Sample data: `assets/sample_data/`
- Packaging sources: `packaging/pyinstaller/`
- Local quality gates: `scripts/quality_gates.py`

## Recommended Validation Flow

1. Install dependencies
2. Run baseline gates:

```bash
python scripts/quality_gates.py
```

3. For release validation, run full gates:

```bash
python scripts/quality_gates.py --with-build --with-exe-smoke
```

## Developer Boundary

This repository intentionally separates:

- versioned sources/configuration
- generated build/runtime artifacts (`build/`, `dist/`, `output/`)

Generated folders are excluded from version control.
