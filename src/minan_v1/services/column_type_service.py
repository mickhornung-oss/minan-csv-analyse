"""Oeffentliche Hilfsfunktionen fuer Spaltentyp-Klassifizierung."""

import pandas as pd

from minan_v1.config import MAX_UNIQUE_VALUES_FOR_CATEGORICAL
from minan_v1.domain.enums import ColumnType

_ID_KEYWORDS = [
    "id",
    "nr",
    "nummer",
    "number",
    "key",
    "schluessel",
    "code",
    "kennung",
    "ident",
    "identifier",
    "ref",
    "referenz",
    "index",
    "idx",
    "guid",
    "uuid",
]

_MEASURE_EXCLUDE_KEYWORDS = [
    "datum",
    "date",
    "zeit",
    "time",
    "umsatz",
    "preis",
    "price",
    "betrag",
    "amount",
    "alter",
    "age",
    "menge",
    "quantity",
    "rabatt",
    "discount",
    "gewicht",
    "weight",
    "groesse",
    "size",
    "hoehe",
    "height",
    "breite",
    "width",
    "laenge",
    "length",
    "temperatur",
    "temperature",
    "prozent",
    "percent",
    "rate",
    "ratio",
    "score",
    "wert",
    "value",
    "faktor",
    "factor",
]


def classify_column(col: pd.Series) -> ColumnType:
    """Klassifiziert den Spaltentyp."""
    col_name_lower = str(col.name).lower()

    if any(keyword in col_name_lower for keyword in _ID_KEYWORDS):
        non_null = col.dropna()
        if len(non_null) > 0:
            unique_ratio = non_null.nunique() / len(non_null)
            if unique_ratio >= 0.95 and not pd.api.types.is_datetime64_any_dtype(col):
                if pd.api.types.is_numeric_dtype(col):
                    if col.dtype.kind in ["i", "u"] or (
                        col.dtype.kind == "f" and (col % 1 == 0).all()
                    ):
                        return ColumnType.ID
                else:
                    return ColumnType.ID

    if pd.api.types.is_bool_dtype(col):
        return ColumnType.CATEGORICAL

    if pd.api.types.is_numeric_dtype(col):
        return ColumnType.NUMERIC

    if pd.api.types.is_datetime64_any_dtype(col):
        return ColumnType.DATETIME

    if pd.api.types.is_object_dtype(col) or pd.api.types.is_string_dtype(col):
        non_null = col.dropna()
        if len(non_null) == 0:
            return ColumnType.UNKNOWN

        if looks_like_datetime(non_null):
            return ColumnType.DATETIME

        unique_ratio = non_null.nunique() / len(non_null)
        if (
            non_null.nunique() <= MAX_UNIQUE_VALUES_FOR_CATEGORICAL
            or unique_ratio < 0.5
        ):
            return ColumnType.CATEGORICAL

        return ColumnType.TEXT

    return ColumnType.UNKNOWN


def is_id_column(
    col: pd.Series,
    col_type: ColumnType,
    unique: int,
    total_rows: int,
) -> bool:
    """Prueft heuristisch, ob eine Spalte als ID einzuordnen ist."""
    if total_rows <= 1:
        return False
    if unique < total_rows * 0.9:
        return False

    col_name_lower = str(col.name).lower()

    if any(keyword in col_name_lower for keyword in _MEASURE_EXCLUDE_KEYWORDS):
        return False

    if col_type == ColumnType.DATETIME:
        return False

    if col_type == ColumnType.NUMERIC:
        non_null = col.dropna()
        if len(non_null) > 0:
            unique_ratio = unique / len(non_null)
            if unique_ratio > 0.95:
                if non_null.dtype.kind in ["i", "u"]:
                    value_range = non_null.max() - non_null.min()
                    if value_range > len(non_null) * 10:
                        return False
                elif non_null.dtype.kind == "f":
                    if (non_null % 1 != 0).any():
                        return False

    has_id_keyword = any(keyword in col_name_lower for keyword in _ID_KEYWORDS)
    if has_id_keyword:
        return unique >= total_rows * 0.95
    return unique >= total_rows * 0.98


def looks_like_datetime(series: pd.Series) -> bool:
    """Prueft, ob eine Stichprobe wie Datumswerte aussieht."""
    sample = series.head(20)
    try:
        parsed = pd.to_datetime(sample, errors="coerce", format="mixed")
        success_rate = parsed.notna().sum() / len(sample)
        return success_rate >= 0.8
    except (TypeError, ValueError):
        return False
