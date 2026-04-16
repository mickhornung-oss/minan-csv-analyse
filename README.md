# MinAn 1.4 — CSV Quick Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/mickhornung-oss/minan-csv-analyse/actions/workflows/python-tests.yml/badge.svg)](https://github.com/mickhornung-oss/minan-csv-analyse/actions)
[![codecov](https://codecov.io/gh/mickhornung-oss/minan-csv-analyse/branch/main/graph/badge.svg)](https://codecov.io/gh/mickhornung-oss/minan-csv-analyse)

Portable Windows desktop tool for rapid CSV analysis — load a file, get an instant structural profile, data quality report, charts, filtered views, and an HTML export. The original file is never modified.

> **Deutsch:** Portables Windows-Desktop-Tool zur schnellen CSV-Analyse mit Strukturprofil, Datenqualitaet, Diagrammen und lokalem HTML-Bericht.

## 📸 Demo

<!-- Add a screenshot here: images/minan-demo.png -->
*Arbeitsansicht mit Filtern, Schnellansichten und Diagrammen.*

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
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
run_dev.bat
```

## Build Portable Release

```batch
build_release.bat
```

Output in `dist/MinAn_1_4/MinAn.exe` — portable, no Python installation needed.

## Tech Stack

- **Python** 3.10+
- **PySide6** — desktop GUI
- **pandas** — data processing
- **matplotlib** — charts
- **PyInstaller** — portable build

## Tests

```bash
pytest tests/ -v
# 155 tests passing
```

Test coverage includes:
- Service unit tests (profile, quality, chart, export, report, transform)
- GUI smoke tests (offscreen, full user flow)
- Stress tests for type detection consistency

## Project Structure

```
src/minan_v1/
├── domain/         # Data models and enums (dataclasses)
├── services/       # Business logic — one service per concern
└── ui/             # PySide6 UI components

tests/              # 17 test files, 155 tests
```

## Topics

`python` `gui` `pandas` `data-analysis` `csv` `data-visualization` `desktop-application` `pyside6`
