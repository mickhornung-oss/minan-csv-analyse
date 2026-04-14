"""CSV-Import-Service: Laden von CSV-Dateien in einen DataFrame."""

from pathlib import Path
from typing import Optional

import pandas as pd

from minan_v1.config import CSV_FALLBACK_ENCODINGS
from minan_v1.domain.models import ImportResult
from minan_v1.utils.csv_sniffer import detect_encoding, detect_separator


def load_csv(path: Path, encoding: Optional[str] = None,
             separator: Optional[str] = None) -> tuple[pd.DataFrame, ImportResult]:
    """Lädt eine CSV-Datei und gibt DataFrame + ImportResult zurück.

    Erkennt Encoding und Separator automatisch, wenn nicht angegeben.
    Überschreibt niemals die Originaldatei.
    """
    result = ImportResult(
        success=False,
        file_path=path,
        file_name=path.name,
    )

    # --- Validierung ---
    if not path.exists():
        result.error = f"Datei nicht gefunden: {path}"
        return pd.DataFrame(), result

    if not path.is_file():
        result.error = f"Kein gültiger Dateipfad: {path}"
        return pd.DataFrame(), result

    if path.stat().st_size == 0:
        result.error = "Die Datei ist leer."
        return pd.DataFrame(), result

    # --- Encoding erkennen ---
    if encoding is None:
        encoding = detect_encoding(path)
    result.encoding = encoding

    # --- Separator erkennen ---
    if separator is None:
        separator = detect_separator(path, encoding)
    result.separator = separator

    # --- CSV laden mit Fallback-Strategie ---
    df = _try_load(path, encoding, separator, result)

    if df is None:
        # Fallback: andere Encodings probieren
        for fallback_enc in CSV_FALLBACK_ENCODINGS:
            if fallback_enc == encoding:
                continue
            df = _try_load(path, fallback_enc, separator, result)
            if df is not None:
                result.encoding = fallback_enc
                result.warnings.append(
                    f"Fallback-Encoding verwendet: {fallback_enc}"
                )
                break

    if df is None:
        result.error = result.error or "CSV konnte mit keinem Encoding geladen werden."
        return pd.DataFrame(), result

    # --- Plausibilitätsprüfung ---
    if df.empty or len(df.columns) == 0:
        result.error = "Keine Spalten erkannt – Datei ist möglicherweise keine gültige CSV."
        result.success = False
        return pd.DataFrame(), result

    if len(df.columns) == 1 and separator != ",":
        # Vielleicht falscher Separator – Warnung
        result.warnings.append(
            "Nur eine Spalte erkannt. Prüfen Sie das Trennzeichen."
        )

    # --- Ergebnis ---
    result.success = True
    result.row_count = len(df)
    result.column_count = len(df.columns)

    return df, result


def _try_load(path: Path, encoding: str, separator: str,
              result: ImportResult) -> Optional[pd.DataFrame]:
    """Versucht eine CSV mit gegebenem Encoding/Separator zu laden."""
    try:
        df = pd.read_csv(
            path,
            sep=separator,
            encoding=encoding,
            on_bad_lines="warn",
            low_memory=False,
        )
        return df
    except UnicodeDecodeError:
        result.error = f"Encoding-Fehler mit {encoding}."
        return None
    except pd.errors.ParserError as e:
        result.error = f"CSV-Parse-Fehler: {e}"
        return None
    except Exception as e:
        result.error = f"Unerwarteter Fehler: {e}"
        return None
