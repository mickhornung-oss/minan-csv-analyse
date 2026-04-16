"""Session-State: Zentrale Datenhaltung einer Analysesitzung."""

from pathlib import Path
from typing import Optional

import pandas as pd

from minan_v1.domain.enums import AnalysisStatus, ColumnType
from minan_v1.domain.models import (
    DatasetProfile,
    ExportResult,
    FilterCondition,
    FilterOperator,
    ImportResult,
    MarkingResult,
    QualityReport,
    ReportResult,
    SortState,
    SummaryResult,
)


class SessionState:
    """Haelt den vollstaendigen Zustand einer Analysesitzung."""

    def __init__(self) -> None:
        self._original_df: Optional[pd.DataFrame] = None
        self._working_df: Optional[pd.DataFrame] = None
        self._view_df: Optional[pd.DataFrame] = None
        self._source_path: Optional[Path] = None
        self._profile: Optional[DatasetProfile] = None
        self._import_result: Optional[ImportResult] = None
        self._quality_report: Optional[QualityReport] = None
        self._summary: Optional[SummaryResult] = None
        self._status: AnalysisStatus = AnalysisStatus.EMPTY
        self._hidden_columns: list[str] = []
        self._active_filters: list[FilterCondition] = []
        self._sort_state: Optional[SortState] = None
        self._duplicate_marking: Optional[MarkingResult] = None
        self._missing_marking: Optional[MarkingResult] = None
        self._last_export: Optional[ExportResult] = None
        self._last_report: Optional[ReportResult] = None
        self._quick_view_mode: Optional[str] = None
        self._manual_column_types: dict[str, ColumnType] = {}

    def load(self, df: pd.DataFrame, source_path: Path) -> None:
        """Laedt einen DataFrame und erzeugt die Arbeitskopie."""
        self._original_df = df
        self._working_df = df.copy()
        self._view_df = self._working_df.copy()
        self._source_path = source_path
        self._status = AnalysisStatus.LOADED

    @property
    def original_df(self) -> Optional[pd.DataFrame]:
        return self._original_df

    @property
    def working_df(self) -> Optional[pd.DataFrame]:
        return self._working_df

    @working_df.setter
    def working_df(self, df: pd.DataFrame) -> None:
        self._working_df = df
        self._rebuild_view()
        self._status = AnalysisStatus.MODIFIED

    @property
    def view_df(self) -> Optional[pd.DataFrame]:
        return self._view_df

    @property
    def current_df(self) -> Optional[pd.DataFrame]:
        return self._view_df

    @property
    def source_path(self) -> Optional[Path]:
        return self._source_path

    @property
    def profile(self) -> Optional[DatasetProfile]:
        return self._profile

    @profile.setter
    def profile(self, value: DatasetProfile) -> None:
        self._profile = value

    @property
    def import_result(self) -> Optional[ImportResult]:
        return self._import_result

    @import_result.setter
    def import_result(self, value: ImportResult) -> None:
        self._import_result = value

    @property
    def quality_report(self) -> Optional[QualityReport]:
        return self._quality_report

    @quality_report.setter
    def quality_report(self, value: QualityReport) -> None:
        self._quality_report = value

    @property
    def summary(self) -> Optional[SummaryResult]:
        return self._summary

    @summary.setter
    def summary(self, value: SummaryResult) -> None:
        self._summary = value

    @property
    def status(self) -> AnalysisStatus:
        return self._status

    @status.setter
    def status(self, value: AnalysisStatus) -> None:
        self._status = value

    @property
    def has_data(self) -> bool:
        return self._working_df is not None

    @property
    def is_modified(self) -> bool:
        if self._original_df is None or self._working_df is None:
            return False
        return not self._original_df.equals(self._working_df)

    @property
    def hidden_columns(self) -> list[str]:
        return self._hidden_columns

    @hidden_columns.setter
    def hidden_columns(self, columns: list[str]) -> None:
        self._hidden_columns = columns
        self._status = AnalysisStatus.MODIFIED

    @property
    def active_filters(self) -> list[FilterCondition]:
        return self._active_filters

    @active_filters.setter
    def active_filters(self, filters: list[FilterCondition]) -> None:
        self._active_filters = filters
        self._rebuild_view()
        self._status = AnalysisStatus.MODIFIED

    @property
    def sort_state(self) -> Optional[SortState]:
        return self._sort_state

    @sort_state.setter
    def sort_state(self, state: Optional[SortState]) -> None:
        self._sort_state = state
        self._status = AnalysisStatus.MODIFIED

    @property
    def duplicate_marking(self) -> Optional[MarkingResult]:
        return self._duplicate_marking

    @duplicate_marking.setter
    def duplicate_marking(self, marking: Optional[MarkingResult]) -> None:
        self._duplicate_marking = marking

    @property
    def missing_marking(self) -> Optional[MarkingResult]:
        return self._missing_marking

    @missing_marking.setter
    def missing_marking(self, marking: Optional[MarkingResult]) -> None:
        self._missing_marking = marking

    @property
    def last_export(self) -> Optional[ExportResult]:
        return self._last_export

    @last_export.setter
    def last_export(self, result: Optional[ExportResult]) -> None:
        self._last_export = result

    @property
    def manual_column_types(self) -> dict[str, ColumnType]:
        return self._manual_column_types

    @manual_column_types.setter
    def manual_column_types(self, types: dict[str, ColumnType]) -> None:
        self._manual_column_types = types
        self._status = AnalysisStatus.MODIFIED

    @property
    def last_report(self) -> Optional[ReportResult]:
        return self._last_report

    @last_report.setter
    def last_report(self, result: Optional[ReportResult]) -> None:
        self._last_report = result

    @property
    def quick_view_mode(self) -> Optional[str]:
        return self._quick_view_mode

    @property
    def has_active_view(self) -> bool:
        return bool(self._active_filters) or self._quick_view_mode is not None

    def reset(self) -> None:
        """Setzt die Sitzung komplett zurueck."""
        self._original_df = None
        self._working_df = None
        self._view_df = None
        self._source_path = None
        self._profile = None
        self._import_result = None
        self._quality_report = None
        self._summary = None
        self._status = AnalysisStatus.EMPTY
        self._hidden_columns = []
        self._active_filters = []
        self._sort_state = None
        self._duplicate_marking = None
        self._missing_marking = None
        self._last_export = None
        self._last_report = None
        self._quick_view_mode = None
        self._manual_column_types = {}

    def revert_to_original(self) -> None:
        """Setzt die Arbeitskopie auf den Originalzustand zurueck."""
        if self._original_df is not None:
            self._working_df = self._original_df.copy()
            self._view_df = self._working_df.copy()
            self._status = AnalysisStatus.LOADED
            self._hidden_columns = []
            self._active_filters = []
            self._sort_state = None
            self._duplicate_marking = None
            self._missing_marking = None
            self._last_report = None
            self._quick_view_mode = None

    def add_filter(self, condition: FilterCondition) -> None:
        self.active_filters = [*self._active_filters, condition]

    def remove_filter_at(self, index: int) -> None:
        if 0 <= index < len(self._active_filters):
            filters = self._active_filters.copy()
            del filters[index]
            self.active_filters = filters

    def clear_filters(self) -> None:
        self.active_filters = []

    def set_quick_view_mode(self, mode: Optional[str]) -> None:
        self._quick_view_mode = mode
        self._rebuild_view()
        self._status = AnalysisStatus.MODIFIED

    def clear_quick_view_mode(self) -> None:
        self.set_quick_view_mode(None)

    def describe_active_view(self) -> str:
        parts: list[str] = []
        if self._active_filters:
            parts.append(f"{len(self._active_filters)} Filter aktiv")
        if self._quick_view_mode == "missing":
            parts.append("Schnellansicht: Fehlende Werte")
        elif self._quick_view_mode == "duplicates":
            parts.append("Schnellansicht: Dubletten")
        elif self._quick_view_mode == "outliers":
            parts.append("Schnellansicht: Ausreisser-Kandidaten")
        return " | ".join(parts) if parts else "Gesamtansicht"

    def active_filter_texts(self) -> list[str]:
        """Gibt lesbare Texte fuer alle aktiven Filter zurueck."""
        return [condition.to_display_text() for condition in self._active_filters]

    def _rebuild_view(self) -> None:
        if self._working_df is None:
            self._view_df = None
            return

        df = self._working_df.copy()
        for condition in self._active_filters:
            df = self._apply_filter_condition(df, condition)

        if self._quick_view_mode == "missing":
            df = df[df.isna().any(axis=1)].copy()
        elif self._quick_view_mode == "duplicates":
            df = df[df.duplicated(keep=False)].copy()
        elif self._quick_view_mode == "outliers":
            df = self._apply_outlier_view(df)

        self._view_df = df

    @staticmethod
    def _apply_filter_condition(
        df: pd.DataFrame, condition: FilterCondition
    ) -> pd.DataFrame:
        if condition.column not in df.columns:
            return df

        series = df[condition.column]
        mask = pd.Series(True, index=df.index)

        if condition.operator == FilterOperator.EQUAL:
            numeric_series = pd.to_numeric(series, errors="coerce")
            try:
                mask = numeric_series == float(condition.value)
                if numeric_series.isna().all():
                    raise ValueError
            except (TypeError, ValueError):
                mask = series.astype(str) == str(condition.value)
        elif condition.operator == FilterOperator.NOT_EQUAL:
            numeric_series = pd.to_numeric(series, errors="coerce")
            try:
                mask = numeric_series != float(condition.value)
                if numeric_series.isna().all():
                    raise ValueError
            except (TypeError, ValueError):
                mask = series.astype(str) != str(condition.value)
        elif condition.operator == FilterOperator.GREATER_THAN:
            mask = pd.to_numeric(series, errors="coerce") > float(condition.value)
        elif condition.operator == FilterOperator.LESS_THAN:
            mask = pd.to_numeric(series, errors="coerce") < float(condition.value)
        elif condition.operator == FilterOperator.BETWEEN:
            numeric_series = pd.to_numeric(series, errors="coerce")
            low = float(condition.value)
            high = float(condition.value2)
            mask = (numeric_series >= low) & (numeric_series <= high)
        elif condition.operator == FilterOperator.CONTAINS:
            mask = series.astype(str).str.contains(
                str(condition.value), na=False, regex=False
            )
        elif condition.operator == FilterOperator.STARTS_WITH:
            mask = series.astype(str).str.startswith(str(condition.value), na=False)
        elif condition.operator == FilterOperator.IS_EMPTY:
            mask = series.isna()
        elif condition.operator == FilterOperator.IS_NOT_EMPTY:
            mask = ~series.isna()

        return df[mask].copy()

    @staticmethod
    def _apply_outlier_view(df: pd.DataFrame) -> pd.DataFrame:
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.empty:
            return df.iloc[0:0].copy()

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
            col_mask = numeric_df[column].lt(lower) | numeric_df[column].gt(upper)
            candidate_mask = candidate_mask | col_mask.fillna(False)

        return df[candidate_mask].copy()
