"""Zugriff auf portable Ressourcen- und Output-Pfade."""

from pathlib import Path
import sys

from minan_v1.config import (
    DEV_SAMPLE_DATA_DIR,
    ICONS_DIR,
    IS_FROZEN,
    OUTPUT_CSV_DIR,
    OUTPUT_DIR,
    OUTPUT_REPORTS_DIR,
    RELEASE_INTERNAL_SAMPLE_DATA_DIR,
    RUNTIME_ROOT,
    SAMPLE_FILE_NAME,
    SHORTSTART_README_PATH,
)

BUNDLED_ROOT = Path(getattr(sys, "_MEIPASS", RUNTIME_ROOT))
BUNDLED_ICONS_DIR = BUNDLED_ROOT / "assets" / "icons"


def icon_path(name: str) -> Path:
    bundled_icon = BUNDLED_ICONS_DIR / name
    if bundled_icon.exists():
        return bundled_icon
    return ICONS_DIR / name


def runtime_root() -> Path:
    return RUNTIME_ROOT


def sample_data_dir() -> Path:
    release_file = RELEASE_INTERNAL_SAMPLE_DATA_DIR / SAMPLE_FILE_NAME
    if release_file.exists():
        return RELEASE_INTERNAL_SAMPLE_DATA_DIR
    return DEV_SAMPLE_DATA_DIR


def release_sample_data_dir() -> Path:
    return RELEASE_INTERNAL_SAMPLE_DATA_DIR


def sample_data_path(name: str = SAMPLE_FILE_NAME) -> Path:
    return sample_data_dir() / name


def default_csv_export_dir() -> Path:
    return OUTPUT_CSV_DIR


def default_report_dir() -> Path:
    return OUTPUT_REPORTS_DIR


def default_csv_export_path(filename: str) -> Path:
    return default_csv_export_dir() / filename


def default_report_path(filename: str) -> Path:
    return default_report_dir() / filename


def shortstart_readme_path() -> Path:
    return SHORTSTART_README_PATH


def ensure_runtime_dirs() -> None:
    """Stellt benoetigte Laufzeitordner fuer Output und Release-Samples sicher."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_CSV_DIR.mkdir(parents=True, exist_ok=True)
    if IS_FROZEN:
        RELEASE_INTERNAL_SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)


def is_internal_path(path: Path) -> bool:
    """Prueft, ob ein Pfad in _internal liegt."""
    try:
        return "_internal" in {part.lower() for part in path.resolve().parts}
    except FileNotFoundError:
        return "_internal" in {part.lower() for part in path.parts}
