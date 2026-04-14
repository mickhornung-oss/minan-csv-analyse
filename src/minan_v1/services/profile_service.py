"""Profil-Service: Erstueberblick und Strukturprofil eines DataFrames."""

import numpy as np
import pandas as pd

from minan_v1.config import TOP_N_VALUES
from minan_v1.domain.enums import ColumnType
from minan_v1.domain.models import ColumnProfile, DatasetProfile
from minan_v1.services.column_type_service import classify_column, is_id_column


def create_profile(df: pd.DataFrame, manual_types: dict = None) -> DatasetProfile:
    """Erstellt ein Strukturprofil des DataFrames."""
    if manual_types is None:
        manual_types = {}

    profile = DatasetProfile(
        row_count=len(df),
        column_count=len(df.columns),
        duplicate_rows=int(df.duplicated().sum()),
        total_missing=int(df.isna().sum().sum()),
    )

    for col_name in df.columns:
        col = df[col_name]
        col_type = manual_types.get(col_name, classify_column(col))
        cp = _profile_column(col, len(df), col_type)
        profile.columns.append(cp)

    profile.numeric_columns = sum(
        1 for c in profile.columns if c.column_type == ColumnType.NUMERIC
    )
    profile.categorical_columns = sum(
        1 for c in profile.columns if c.column_type == ColumnType.CATEGORICAL
    )
    profile.datetime_columns = sum(
        1 for c in profile.columns if c.column_type == ColumnType.DATETIME
    )
    profile.id_columns = sum(
        1 for c in profile.columns if c.column_type == ColumnType.ID
    )
    profile.text_columns = sum(
        1 for c in profile.columns if c.column_type == ColumnType.TEXT
    )
    profile.unknown_columns = sum(
        1 for c in profile.columns if c.column_type == ColumnType.UNKNOWN
    )
    profile.boolean_columns = sum(
        1
        for c in profile.columns
        if c.column_type == ColumnType.CATEGORICAL and c.unique <= 2 and c.missing == 0
    )
    return profile


def _profile_column(
    col: pd.Series,
    total_rows: int,
    col_type: ColumnType = None,
) -> ColumnProfile:
    """Erstellt das Profil einer einzelnen Spalte."""
    if col_type is None:
        col_type = classify_column(col)

    missing = int(col.isna().sum())
    count = total_rows - missing
    unique = int(col.nunique(dropna=True))
    missing_pct = (missing / total_rows * 100) if total_rows > 0 else 0.0
    is_id_like = is_id_column(col, col_type, unique, total_rows)

    cp = ColumnProfile(
        name=str(col.name),
        dtype=str(col.dtype),
        column_type=col_type,
        count=count,
        missing=missing,
        missing_pct=round(missing_pct, 1),
        unique=unique,
        is_constant=(unique <= 1 and missing == 0),
        is_id_like=is_id_like,
    )

    non_null = col.dropna()
    if len(non_null) > 0:
        cp.sample_values = [str(v) for v in non_null.head(5).tolist()]

    if unique > 0:
        top = col.value_counts(dropna=True).head(TOP_N_VALUES)
        cp.top_values = [(str(k), int(v)) for k, v in top.items()]

    if col_type == ColumnType.NUMERIC and count > 0:
        numeric = col.dropna()
        if pd.api.types.is_numeric_dtype(numeric):
            cp.mean = _safe_float(numeric.mean())
            cp.median = _safe_float(numeric.median())
            cp.std = _safe_float(numeric.std())
            cp.min_val = _safe_float(numeric.min())
            cp.max_val = _safe_float(numeric.max())
            try:
                cp.q1 = _safe_float(numeric.quantile(0.25))
                cp.q3 = _safe_float(numeric.quantile(0.75))
            except (TypeError, ValueError):
                cp.q1 = None
                cp.q3 = None
    return cp


def _safe_float(val) -> float:
    """Konvertiert einen Wert sicher zu float."""
    try:
        f = float(val)
        if np.isnan(f) or np.isinf(f):
            return None
        return round(f, 4)
    except (TypeError, ValueError):
        return None
