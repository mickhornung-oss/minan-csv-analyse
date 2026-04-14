"""Datei-Hilfsfunktionen: Pfadvalidierung, sichere Pfade."""

from pathlib import Path


def safe_export_path(original: Path, suffix: str = "_export") -> Path:
    """Erzeugt einen sicheren Exportpfad, der das Original nicht überschreibt."""
    stem = original.stem
    parent = original.parent
    new_name = f"{stem}{suffix}.csv"
    return parent / new_name


def file_size_readable(size_bytes: int) -> str:
    """Gibt eine lesbare Dateigröße zurück (z.B. '1.2 MB')."""
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
