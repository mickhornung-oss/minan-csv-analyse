"""Validierungsfunktionen für Benutzereingaben und Dateipfade."""

from pathlib import Path


def is_valid_csv_path(path: Path) -> bool:
    """Prüft ob der Pfad auf eine existierende CSV-Datei zeigt."""
    return path.exists() and path.is_file() and path.suffix.lower() == ".csv"


def is_valid_export_path(path: Path) -> bool:
    """Prüft ob der Exportpfad gültig ist (Verzeichnis existiert, kein Überschreiben)."""
    return path.parent.exists() and path.suffix.lower() == ".csv"
