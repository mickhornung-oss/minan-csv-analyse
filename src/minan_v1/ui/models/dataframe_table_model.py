"""Qt-TableModel-Adapter für pandas DataFrames."""

from typing import Any, Optional

import pandas as pd
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class DataFrameTableModel(QAbstractTableModel):
    """Bildet einen pandas DataFrame auf ein Qt-TableModel ab."""

    def __init__(self, df: Optional[pd.DataFrame] = None, parent=None) -> None:
        super().__init__(parent)
        self._df = df if df is not None else pd.DataFrame()
        self._duplicate_rows: set[Any] = set()
        self._missing_cells: set[tuple[Any, str]] = set()
        self._show_duplicate_marking = False
        self._show_missing_marking = False

    def set_dataframe(self, df: pd.DataFrame) -> None:
        """Setzt einen neuen DataFrame und aktualisiert die View."""
        self.beginResetModel()
        self._df = df
        self._duplicate_rows.clear()
        self._missing_cells.clear()
        self.endResetModel()

    def set_markings(
        self,
        duplicate_indices: list[Any],
        missing_cells: list[tuple[Any, str]],
        show_duplicates: bool,
        show_missing: bool,
    ) -> None:
        """Setzt die aktiven Markierungen und aktualisiert die View."""
        self.beginResetModel()
        self._duplicate_rows = set(duplicate_indices)
        self._missing_cells = set(missing_cells)
        self._show_duplicate_marking = show_duplicates
        self._show_missing_marking = show_missing
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._df)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._df.columns)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None

        row_idx = index.row()
        col_idx = index.column()

        # Prüfe ob der Wert fehlt
        value = self._df.iloc[row_idx, col_idx]
        data_index = self._df.index[row_idx]
        column_name = self._df.columns[col_idx]
        is_missing = (
            self._show_missing_marking
            and (data_index, column_name) in self._missing_cells
        )
        is_duplicate = (
            self._show_duplicate_marking and data_index in self._duplicate_rows
        )

        if role == Qt.DisplayRole:
            if pd.isna(value):
                return ""
            return str(value)

        if role == Qt.ForegroundRole:
            from PySide6.QtGui import QColor

            if is_missing:
                # Graue Textfarbe für fehlende Werte
                return QColor(180, 180, 180)
            if is_duplicate:
                # Dunkelrote Textfarbe für Dubletten
                return QColor(200, 50, 50)
            return None

        if role == Qt.BackgroundRole:
            from PySide6.QtGui import QColor

            if is_missing:
                # Dezenter gelblicher Hintergrund für fehlende Werte
                return QColor(255, 255, 230)
            if is_duplicate and not is_missing:
                # Dezenter rötlicher Hintergrund für Dubletten
                return QColor(255, 245, 245)
            return None

        if role == Qt.ToolTipRole:
            if is_missing:
                return "(leer)"
            if is_duplicate:
                return "(Dublette)"
            return str(value)

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole
    ) -> Any:
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if 0 <= section < len(self._df.columns):
                return str(self._df.columns[section])
        else:
            return str(section + 1)

        return None
