"""Tabellen-Panel: Zeigt die Daten als scrollbare Tabellenvorschau."""

from typing import Optional

import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QLabel, QTableView, QVBoxLayout, QWidget

from minan_v1.ui.models.dataframe_table_model import DataFrameTableModel


class TablePanel(QWidget):
    """Panel für die tabellarische Vorschau der Arbeitskopie."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._model = DataFrameTableModel()
        self._hidden_columns: list[str] = []
        self._duplicate_indices: list[int] = []
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self._info_label = QLabel("Noch keine Daten geladen.")
        self._info_label.setObjectName("sectionHintLabel")
        layout.addWidget(self._info_label)

        self._table_view = QTableView()
        self._table_view.setModel(self._model)
        self._table_view.setAlternatingRowColors(True)
        self._table_view.setSortingEnabled(False)
        self._table_view.setSelectionBehavior(QTableView.SelectRows)
        self._table_view.horizontalHeader().setStretchLastSection(True)
        self._table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )
        self._table_view.verticalHeader().setDefaultSectionSize(26)
        layout.addWidget(self._table_view)

    def set_dataframe(
        self,
        df: pd.DataFrame,
        hidden_columns: Optional[list[str]] = None,
        duplicate_indices: Optional[list[int]] = None,
        missing_cells: Optional[list[tuple[int, str]]] = None,
        show_duplicate_marking: bool = False,
        show_missing_marking: bool = False,
    ) -> None:
        """Setzt den angezeigten DataFrame und optional ausgeblendete Spalten und Dubletten-Indizes.

        Args:
            df: Der anzuzeigende DataFrame
            hidden_columns: Liste der ausgeblendeten Spalten
            duplicate_indices: Liste der Zeilenindizes mit Dubletten
            missing_cells: Liste markierter Fehlwertzellen
            show_duplicate_marking: Dubletten visuell hervorheben
            show_missing_marking: Fehlwerte visuell hervorheben
        """
        if hidden_columns is None:
            hidden_columns = []
        if duplicate_indices is None:
            duplicate_indices = []
        if missing_cells is None:
            missing_cells = []

        self._hidden_columns = hidden_columns
        self._duplicate_indices = duplicate_indices

        # Ausgeblendete Spalten entfernen
        display_df = df.copy()
        if hidden_columns:
            columns_to_drop = [
                col for col in hidden_columns if col in display_df.columns
            ]
            if columns_to_drop:
                display_df = display_df.drop(columns=columns_to_drop)

        self._model.set_dataframe(display_df)
        self._model.set_markings(
            duplicate_indices,
            missing_cells,
            show_duplicate_marking,
            show_missing_marking,
        )

        # Info-Label aktualisieren
        total_cols = len(df.columns)
        visible_cols = len(display_df.columns)
        if hidden_columns:
            self._info_label.setText(
                f"{len(df)} Zeilen, {visible_cols} von {total_cols} Spalten sichtbar"
            )
        else:
            self._info_label.setText(f"{len(df)} Zeilen, {total_cols} Spalten")

    def refresh_view(
        self, df: pd.DataFrame, duplicate_indices: Optional[list[int]] = None
    ) -> None:
        """Aktualisiert die Ansicht mit dem aktuellen DataFrame.

        Args:
            df: Der aktualisierte DataFrame
            duplicate_indices: Optionale Liste der Zeilenindizes mit Dubletten
        """
        if duplicate_indices is None:
            duplicate_indices = self._duplicate_indices
        self.set_dataframe(df, self._hidden_columns, duplicate_indices)
