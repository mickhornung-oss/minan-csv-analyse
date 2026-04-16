# MinAn 1.4 - CSV Quick Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/mickhornung-oss/minan-csv-analyse/actions/workflows/python-tests.yml/badge.svg)](https://github.com/mickhornung-oss/minan-csv-analyse/actions/workflows/python-tests.yml)

Portable Windows desktop tool for rapid CSV analysis. Load a file and get structural profiling, data quality checks, charts, filtered views, and a local HTML report export. The source CSV is not modified.

## Demo

Screenshot will be added after the next UI capture update.

## Features

| Feature | Details |
|---|---|
| CSV Loading | Auto-detects encoding and separator |
| Structural Profile | Column types, missing values, cardinality |
| Data Quality Report | Duplicates, empty columns, high-missing detection |
| Charts | Histograms, bar charts, distribution plots |
| Filtered Views | Multi-filter with type overrides |
| CSV Export | Export the active filtered view |
| HTML Report | Local analysis report from active view |
| Portable Build | Single `.exe`, no installation required |

## Quick Start (Dev Mode)

```batch
pip install -r requirements.txt
run_dev.bat
```

## Build Portable Release

```batch
build_release.bat
```

Output: `dist/MinAn_1_4/MinAn.exe` (portable, no Python installation needed).

## Tech Stack

- Python 3.10+
- PySide6
- pandas
- matplotlib
- PyInstaller

## Tests

```bash
pytest tests/ -v
```

Current suite size: 155 tests.

## Project Structure

```text
src/minan_v1/
|-- domain/      # Data models and enums
|-- services/    # Business logic services
`-- ui/          # PySide6 UI components

tests/           # Test suite
```

## Topics

`python` `gui` `pandas` `data-analysis` `csv` `data-visualization` `desktop-application` `pyside6`
