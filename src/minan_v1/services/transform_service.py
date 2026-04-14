"""Transform-Service: Einfache Bearbeitungen auf der Arbeitskopie."""

import pandas as pd

from minan_v1.domain.models import (
    FilterCondition,
    FilterOperator,
    MarkingResult,
    SortState,
    TransformResult,
)


def rename_column(df: pd.DataFrame, old_name: str, new_name: str) -> TransformResult:
    """Benennt eine Spalte in der Arbeitskopie um."""
    if old_name not in df.columns:
        return TransformResult(success=False, message=f"Spalte '{old_name}' nicht gefunden.")

    if new_name in df.columns and new_name != old_name:
        return TransformResult(success=False, message=f"Spalte '{new_name}' existiert bereits.")

    try:
        renamed_df = df.rename(columns={old_name: new_name})
        return TransformResult(
            success=True,
            message=f"Spalte '{old_name}' in '{new_name}' umbenannt.",
            row_count=len(renamed_df),
            column_count=len(renamed_df.columns),
            df=renamed_df,
        )
    except Exception as exc:
        return TransformResult(success=False, message=f"Fehler beim Umbenennen: {exc}")


def drop_column(df: pd.DataFrame, column: str) -> TransformResult:
    """Entfernt eine Spalte aus der Arbeitskopie."""
    if column not in df.columns:
        return TransformResult(success=False, message=f"Spalte '{column}' nicht gefunden.")

    try:
        dropped_df = df.drop(columns=[column])
        return TransformResult(
            success=True,
            message=f"Spalte '{column}' entfernt.",
            row_count=len(dropped_df),
            column_count=len(dropped_df.columns),
            df=dropped_df,
        )
    except Exception as exc:
        return TransformResult(success=False, message=f"Fehler beim Entfernen: {exc}")


def apply_filter(df: pd.DataFrame, condition: FilterCondition) -> TransformResult:
    """Wendet einen einzelnen Filter auf einen DataFrame an."""
    if condition.column not in df.columns:
        return TransformResult(success=False, message=f"Spalte '{condition.column}' nicht gefunden.")

    try:
        filtered_df = _apply_filter_condition(df, condition)
        return TransformResult(
            success=True,
            message=f"Filter angewendet: {len(filtered_df)} von {len(df)} Zeilen.",
            row_count=len(filtered_df),
            column_count=len(filtered_df.columns),
            df=filtered_df,
        )
    except ValueError as exc:
        return TransformResult(success=False, message=str(exc))
    except Exception as exc:
        return TransformResult(success=False, message=f"Fehler beim Filtern: {exc}")


def apply_filters(df: pd.DataFrame, conditions: list[FilterCondition]) -> TransformResult:
    """Wendet mehrere Filter nacheinander an."""
    try:
        filtered_df = df.copy()
        for condition in conditions:
            single_result = apply_filter(filtered_df, condition)
            if not single_result.success or single_result.df is None:
                return single_result
            filtered_df = single_result.df

        return TransformResult(
            success=True,
            message=f"{len(conditions)} Filter aktiv: {len(filtered_df)} von {len(df)} Zeilen.",
            row_count=len(filtered_df),
            column_count=len(filtered_df.columns),
            df=filtered_df,
        )
    except Exception as exc:
        return TransformResult(success=False, message=f"Fehler beim Filtern: {exc}")


def apply_sort(df: pd.DataFrame, sort_state: SortState) -> TransformResult:
    """Wendet eine Sortierung auf die Arbeitskopie an."""
    if sort_state.column not in df.columns:
        return TransformResult(success=False, message=f"Spalte '{sort_state.column}' nicht gefunden.")

    try:
        df_sorted = df.sort_values(
            by=sort_state.column,
            ascending=sort_state.ascending,
            na_position="last",
        )
        direction = "aufsteigend" if sort_state.ascending else "absteigend"
        return TransformResult(
            success=True,
            message=f"Nach '{sort_state.column}' {direction} sortiert.",
            row_count=len(df_sorted),
            column_count=len(df_sorted.columns),
            df=df_sorted,
        )
    except Exception as exc:
        return TransformResult(success=False, message=f"Fehler beim Sortieren: {exc}")


def mark_duplicates(df: pd.DataFrame) -> MarkingResult:
    """Markiert Dubletten im DataFrame."""
    try:
        duplicates = df.duplicated(keep=False)
        marked_rows = df[duplicates].index.tolist()
        return MarkingResult(
            marked_rows=marked_rows,
            message=f"{len(marked_rows)} Zeilen sind Dubletten (inkl. Original).",
        )
    except Exception as exc:
        return MarkingResult(message=f"Fehler beim Markieren von Dubletten: {exc}")


def mark_missing(df: pd.DataFrame) -> MarkingResult:
    """Markiert fehlende Werte im DataFrame."""
    try:
        marked_cells: list[tuple[int, str]] = []
        marked_columns: list[str] = []

        for col in df.columns:
            missing_mask = df[col].isna()
            if missing_mask.any():
                marked_columns.append(col)
                for row_idx in df[missing_mask].index.tolist():
                    marked_cells.append((row_idx, col))

        return MarkingResult(
            marked_columns=marked_columns,
            marked_cells=marked_cells,
            message=f"{len(marked_cells)} fehlende Werte in {len(marked_columns)} Spalten gefunden.",
        )
    except Exception as exc:
        return MarkingResult(message=f"Fehler beim Markieren von Fehlwerten: {exc}")


def focus_missing_rows(df: pd.DataFrame) -> TransformResult:
    """Erzeugt eine Fokusansicht fuer Zeilen mit mindestens einem Fehlwert."""
    focused_df = df[df.isna().any(axis=1)].copy()
    return TransformResult(
        success=True,
        message=f"Schnellansicht Fehlwerte: {len(focused_df)} Zeilen.",
        row_count=len(focused_df),
        column_count=len(focused_df.columns),
        df=focused_df,
    )


def focus_duplicate_rows(df: pd.DataFrame) -> TransformResult:
    """Erzeugt eine Fokusansicht fuer alle Dubletten inklusive Originalen."""
    focused_df = df[df.duplicated(keep=False)].copy()
    return TransformResult(
        success=True,
        message=f"Schnellansicht Dubletten: {len(focused_df)} Zeilen.",
        row_count=len(focused_df),
        column_count=len(focused_df.columns),
        df=focused_df,
    )


def focus_outlier_candidates(df: pd.DataFrame) -> TransformResult:
    """Erzeugt eine einfache IQR-basierte Fokusansicht fuer Ausreisser-Kandidaten."""
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        focused_df = df.iloc[0:0].copy()
        return TransformResult(
            success=True,
            message="Schnellansicht Ausreisser: keine numerischen Spalten vorhanden.",
            row_count=0,
            column_count=len(df.columns),
            df=focused_df,
        )

    candidate_mask = pd.Series(False, index=df.index)
    for column in numeric_df.columns:
        series = numeric_df[column].dropna()
        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if pd.isna(iqr):
            continue

        if iqr == 0:
            lower = q1
            upper = q3
        else:
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

        column_mask = numeric_df[column].lt(lower) | numeric_df[column].gt(upper)
        candidate_mask = candidate_mask | column_mask.fillna(False)

    focused_df = df[candidate_mask].copy()
    return TransformResult(
        success=True,
        message=f"Schnellansicht Ausreisser: {len(focused_df)} Kandidatenzeilen.",
        row_count=len(focused_df),
        column_count=len(focused_df.columns),
        df=focused_df,
    )


def _apply_filter_condition(df: pd.DataFrame, condition: FilterCondition) -> pd.DataFrame:
    series = df[condition.column]

    if condition.operator == FilterOperator.EQUAL:
        return df[_build_equality_mask(series, condition.value, negate=False)].copy()

    if condition.operator == FilterOperator.NOT_EQUAL:
        return df[_build_equality_mask(series, condition.value, negate=True)].copy()

    if condition.operator == FilterOperator.GREATER_THAN:
        value = _to_float(condition.value)
        mask = pd.to_numeric(series, errors="coerce") > value
        return df[mask].copy()

    if condition.operator == FilterOperator.LESS_THAN:
        value = _to_float(condition.value)
        mask = pd.to_numeric(series, errors="coerce") < value
        return df[mask].copy()

    if condition.operator == FilterOperator.BETWEEN:
        low = _to_float(condition.value)
        high = _to_float(condition.value2)
        numeric_series = pd.to_numeric(series, errors="coerce")
        mask = (numeric_series >= low) & (numeric_series <= high)
        return df[mask].copy()

    if condition.operator == FilterOperator.CONTAINS:
        mask = series.astype(str).str.contains(str(condition.value), na=False, regex=False)
        return df[mask].copy()

    if condition.operator == FilterOperator.STARTS_WITH:
        mask = series.astype(str).str.startswith(str(condition.value), na=False)
        return df[mask].copy()

    if condition.operator == FilterOperator.IS_EMPTY:
        return df[series.isna()].copy()

    if condition.operator == FilterOperator.IS_NOT_EMPTY:
        return df[~series.isna()].copy()

    raise ValueError(f"Unbekannter Operator: {condition.operator}")


def _build_equality_mask(series: pd.Series, raw_value: str, negate: bool) -> pd.Series:
    numeric_series = pd.to_numeric(series, errors="coerce")
    try:
        value = _to_float(raw_value)
        if numeric_series.notna().any():
            mask = numeric_series != value if negate else numeric_series == value
            return mask.fillna(False if not negate else True)
    except ValueError:
        pass

    string_series = series.astype(str)
    return string_series != str(raw_value) if negate else string_series == str(raw_value)


def _to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Ungueltiger numerischer Wert: {value}") from exc
