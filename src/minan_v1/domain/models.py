"""Datenmodelle fuer MinAn 1.4."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

import pandas as pd

from minan_v1.domain.enums import ColumnType


@dataclass
class ColumnProfile:
    """Profil einer einzelnen Spalte."""

    name: str
    dtype: str
    column_type: ColumnType
    count: int = 0
    missing: int = 0
    missing_pct: float = 0.0
    unique: int = 0
    top_values: list = field(default_factory=list)
    sample_values: list = field(default_factory=list)
    is_constant: bool = False
    is_id_like: bool = False
    mean: Optional[float] = None
    median: Optional[float] = None
    std: Optional[float] = None
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    q1: Optional[float] = None
    q3: Optional[float] = None


@dataclass
class DatasetProfile:
    """Gesamtprofil eines geladenen Datensatzes."""

    source_path: Optional[Path] = None
    row_count: int = 0
    column_count: int = 0
    columns: list[ColumnProfile] = field(default_factory=list)
    file_size_bytes: int = 0
    encoding_detected: str = ""
    separator_detected: str = ""
    duplicate_rows: int = 0
    total_missing: int = 0
    numeric_columns: int = 0
    categorical_columns: int = 0
    datetime_columns: int = 0
    id_columns: int = 0
    text_columns: int = 0
    unknown_columns: int = 0
    boolean_columns: int = 0


@dataclass
class ImportResult:
    """Ergebnis eines CSV-Imports."""

    success: bool
    file_path: Optional[Path] = None
    file_name: str = ""
    encoding: str = ""
    separator: str = ""
    row_count: int = 0
    column_count: int = 0
    warnings: list[str] = field(default_factory=list)
    error: str = ""


@dataclass
class QualityFinding:
    """Einzelne Qualitaetsauffaelligkeit."""

    category: str
    severity: str
    message: str
    column: str = ""


@dataclass
class QualityReport:
    """Gesamter Qualitaetsbericht."""

    duplicate_rows: int = 0
    empty_columns: list[str] = field(default_factory=list)
    empty_rows: int = 0
    constant_columns: list[str] = field(default_factory=list)
    high_missing_columns: list[tuple] = field(default_factory=list)
    high_cardinality_columns: list[tuple] = field(default_factory=list)
    findings: list[QualityFinding] = field(default_factory=list)


@dataclass
class SummaryResult:
    """Ergebnis der regelbasierten Kurzzusammenfassung."""

    lines: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(self.lines)


class FilterOperator(Enum):
    """Unterstuetzte Filteroperatoren."""

    EQUAL = "equal"
    NOT_EQUAL = "not_equal"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    BETWEEN = "between"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    IS_EMPTY = "is_empty"
    IS_NOT_EMPTY = "is_not_empty"


@dataclass
class FilterCondition:
    """Filterbedingung fuer eine Spalte."""

    column: str
    operator: FilterOperator
    value: Optional[str] = None
    value2: Optional[str] = None

    def to_display_text(self) -> str:
        """Gibt eine kompakte, lesbare Darstellung der Filterbedingung zurueck."""
        operator_map = {
            FilterOperator.EQUAL: "=",
            FilterOperator.NOT_EQUAL: "!=",
            FilterOperator.GREATER_THAN: ">",
            FilterOperator.LESS_THAN: "<",
            FilterOperator.BETWEEN: "zwischen",
            FilterOperator.CONTAINS: "enthaelt",
            FilterOperator.STARTS_WITH: "beginnt mit",
            FilterOperator.IS_EMPTY: "ist leer",
            FilterOperator.IS_NOT_EMPTY: "ist nicht leer",
        }
        operator_text = operator_map.get(self.operator, self.operator.value)

        if self.operator == FilterOperator.BETWEEN:
            return f"{self.column} {operator_text} {self.value} und {self.value2}"
        if self.operator in (FilterOperator.IS_EMPTY, FilterOperator.IS_NOT_EMPTY):
            return f"{self.column} {operator_text}"
        return f"{self.column} {operator_text} {self.value}"


@dataclass
class SortState:
    """Sortierzustand fuer eine Spalte."""

    column: str
    ascending: bool = True


@dataclass
class TransformResult:
    """Ergebnis einer Transformation."""

    success: bool
    message: str = ""
    row_count: int = 0
    column_count: int = 0
    warnings: list[str] = field(default_factory=list)
    df: Optional[pd.DataFrame] = None


@dataclass
class MarkingResult:
    """Ergebnis einer Markierungsoperation."""

    marked_rows: list[int] = field(default_factory=list)
    marked_columns: list[str] = field(default_factory=list)
    marked_cells: list[tuple[int, str]] = field(default_factory=list)
    message: str = ""


@dataclass
class ExportResult:
    """Ergebnis eines CSV-Exports."""

    success: bool
    file_path: Optional[Path] = None
    row_count: int = 0
    column_count: int = 0
    warnings: list[str] = field(default_factory=list)
    error: str = ""


@dataclass
class ReportChart:
    """Diagramm-Snapshot fuer den HTML-Bericht."""

    title: str
    image_base64: str


@dataclass
class ReportResult:
    """Ergebnis eines Berichtsexports."""

    success: bool
    file_path: Optional[Path] = None
    view_name: str = ""
    row_count: int = 0
    column_count: int = 0
    charts: list[ReportChart] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error: str = ""
