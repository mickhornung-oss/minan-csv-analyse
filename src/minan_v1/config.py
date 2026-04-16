"""Zentrale Konfiguration und portable Pfade fuer MinAn 1.4."""

import sys
from pathlib import Path

# --- App-Metadaten ---
APP_NAME = "MinAn"
APP_VERSION = "1.4"
APP_VERSION_INFO = "1.4.0.0"
APP_PRODUCT_NAME = "MinAn 1.4"
APP_TITLE = "MinAn 1.4 - CSV-Schnellanalyse"
APP_DESCRIPTION = "Lokales Tool fuer CSV-Schnellanalyse"
APP_COMPANY = "MinAn Software"
REPORT_TITLE = "MinAn 1.4 - Analysebericht"

# --- Projekt-/Laufzeitpfade ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
IS_FROZEN = getattr(sys, "frozen", False)
RUNTIME_ROOT = Path(sys.executable).resolve().parent if IS_FROZEN else PROJECT_ROOT

ASSETS_DIR = PROJECT_ROOT / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
DEV_SAMPLE_DATA_DIR = ASSETS_DIR / "sample_data"

RELEASE_INTERNAL_DIR = RUNTIME_ROOT / "_internal"
RELEASE_INTERNAL_SAMPLE_DATA_DIR = RELEASE_INTERNAL_DIR / "sample_data"
OUTPUT_DIR = RUNTIME_ROOT / "output"
OUTPUT_REPORTS_DIR = OUTPUT_DIR / "reports"
OUTPUT_CSV_DIR = OUTPUT_DIR / "csv"
SHORTSTART_README_PATH = RUNTIME_ROOT / "README_Kurzstart.txt"
SAMPLE_FILE_NAME = "test_csv_deutsch_200x15.csv"

# --- CSV-Import-Defaults ---
CSV_DEFAULT_ENCODING = "utf-8"
CSV_FALLBACK_ENCODINGS = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]
CSV_MAX_PREVIEW_ROWS = 100
CSV_SNIFF_BYTES = 8192

# --- Analyse-Defaults ---
MAX_UNIQUE_VALUES_FOR_CATEGORICAL = 50
HISTOGRAM_BINS = 20
TOP_N_VALUES = 10

# --- UI-Defaults ---
WINDOW_MIN_WIDTH = 1024
WINDOW_MIN_HEIGHT = 680
TABLE_PAGE_SIZE = 200

# --- Export-Defaults ---
EXPORT_DEFAULT_ENCODING = "utf-8"
EXPORT_DEFAULT_SEPARATOR = ","
