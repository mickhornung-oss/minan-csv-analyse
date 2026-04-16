"""Zentrale Enums fuer MinAn 1.4."""

from enum import Enum, auto


class ColumnType(Enum):
    """Erkannter Spaltentyp nach Profilierung."""

    NUMERIC = auto()
    CATEGORICAL = auto()
    DATETIME = auto()
    ID = auto()  # Identifikator-Spalten
    TEXT = auto()
    UNKNOWN = auto()


class AnalysisStatus(Enum):
    """Status der aktuellen Analysesitzung."""

    EMPTY = auto()
    LOADED = auto()
    ANALYZED = auto()
    MODIFIED = auto()
    EXPORTED = auto()
