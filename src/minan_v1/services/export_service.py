"""Export-Service: Export der Arbeitskopie als neue CSV-Datei."""

from pathlib import Path

import pandas as pd

from minan_v1.config import EXPORT_DEFAULT_ENCODING, EXPORT_DEFAULT_SEPARATOR
from minan_v1.domain.models import ExportResult
from minan_v1.resources import ensure_runtime_dirs


def export_csv(
    df: pd.DataFrame,
    target_path: Path,
    encoding: str = EXPORT_DEFAULT_ENCODING,
    separator: str = EXPORT_DEFAULT_SEPARATOR,
    hidden_columns: list[str] = None,
) -> ExportResult:
    """Exportiert den DataFrame als neue CSV-Datei."""
    ensure_runtime_dirs()

    if hidden_columns is None:
        hidden_columns = []

    if df is None or df.empty:
        return ExportResult(success=False, error="Keine Daten zum Export vorhanden.")

    if target_path is None:
        return ExportResult(success=False, error="Kein Zielpfad angegeben.")

    if target_path.suffix.lower() != ".csv":
        target_path = target_path.with_suffix(".csv")

    target_path.parent.mkdir(parents=True, exist_ok=True)

    export_df = df.copy()
    if hidden_columns:
        columns_to_drop = [col for col in hidden_columns if col in export_df.columns]
        if columns_to_drop:
            export_df = export_df.drop(columns=columns_to_drop)

    if export_df.empty:
        return ExportResult(success=False, error="Alle Spalten sind ausgeblendet. Nichts zu exportieren.")

    try:
        export_df.to_csv(target_path, sep=separator, encoding=encoding, index=False)
        return ExportResult(
            success=True,
            file_path=target_path,
            row_count=len(export_df),
            column_count=len(export_df.columns),
        )
    except PermissionError:
        return ExportResult(success=False, error=f"Keine Berechtigung zum Schreiben nach '{target_path}'.")
    except Exception as exc:
        return ExportResult(success=False, error=f"Fehler beim Export: {exc}")
