"""Kennzahlen-Panel: Zeigt Standardkennzahlen pro Spalte in Tabellenform."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem,
    QLabel, QHeaderView,
)
from PySide6.QtCore import Qt

from minan_v1.domain.enums import ColumnType
from minan_v1.domain.models import DatasetProfile


class MetricsPanel(QWidget):
    """Panel für die tabellarische Kennzahlen-Ansicht."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self._placeholder = QLabel("CSV-Datei laden, um Kennzahlen zu sehen.")
        self._placeholder.setObjectName("sectionHintLabel")
        layout.addWidget(self._placeholder)

        self._sub_tabs = QTabWidget()
        self._sub_tabs.hide()
        layout.addWidget(self._sub_tabs)

    def update_metrics(self, profile: DatasetProfile) -> None:
        """Aktualisiert die Kennzahlen-Ansicht aus dem Profil."""
        self._placeholder.hide()
        self._sub_tabs.show()

        # Alte Tabs entfernen
        while self._sub_tabs.count():
            self._sub_tabs.removeTab(0)

        numeric = [c for c in profile.columns if c.column_type == ColumnType.NUMERIC]
        categorical = [c for c in profile.columns
                       if c.column_type == ColumnType.CATEGORICAL]

        if numeric:
            self._sub_tabs.addTab(
                self._build_numeric_table(numeric, profile.row_count),
                f"Numerisch ({len(numeric)})"
            )

        if categorical:
            self._sub_tabs.addTab(
                self._build_categorical_table(categorical, profile.row_count),
                f"Kategorisch ({len(categorical)})"
            )

        if not numeric and not categorical:
            empty = QLabel("Keine numerischen oder kategorialen Spalten vorhanden.")
            empty.setAlignment(Qt.AlignCenter)
            self._sub_tabs.addTab(empty, "Keine Daten")

    def _build_numeric_table(self, columns, row_count: int) -> QTableWidget:
        """Erstellt die Tabelle für numerische Kennzahlen."""
        headers = [
            "Spalte", "Gültig", "Fehlend %", "Mean", "Median", "Min", "Max", "Std", "Q1", "Q3",
        ]
        table = QTableWidget(len(columns), len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Kompakte Spaltenbreiten: Name variabel, Rest fest
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Spaltenname
        for col_idx in range(1, len(headers)):
            table.horizontalHeader().setSectionResizeMode(col_idx, QHeaderView.ResizeToContents)

        # Row-Höhe und Abstände für saubere Anzeige
        table.verticalHeader().setDefaultSectionSize(26)
        table.horizontalHeader().setDefaultSectionSize(80)
        table.setContentsMargins(0, 0, 0, 0)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        for row, col in enumerate(columns):
            items = [
                col.name,
                str(col.count),
                f"{col.missing_pct}%",
                self._fmt(col.mean),
                self._fmt(col.median),
                self._fmt(col.min_val),
                self._fmt(col.max_val),
                self._fmt(col.std),
                self._fmt(col.q1),
                self._fmt(col.q3),
            ]
            for c, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                # Zahlenfelder rechts ausrichten
                if c >= 1:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                table.setItem(row, c, item)

        return table

    def _build_categorical_table(self, columns, row_count: int) -> QTableWidget:
        """Erstellt die Tabelle für kategoriale Kennzahlen."""
        headers = [
            "Spalte", "Gültig", "Fehlend %", "Unique", "Top-Werte",
        ]
        table = QTableWidget(len(columns), len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Kompakte Spaltenbreiten: Name und Top-Werte variabel, Rest fest
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Spaltenname
        for col_idx in range(1, 4):
            table.horizontalHeader().setSectionResizeMode(col_idx, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)  # Top-Werte

        # Row-Höhe und Abstände für saubere Anzeige
        table.verticalHeader().setDefaultSectionSize(26)
        table.horizontalHeader().setDefaultSectionSize(80)
        table.setContentsMargins(0, 0, 0, 0)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        for row, col in enumerate(columns):
            top_str = ", ".join(
                f"{name} ({count})" for name, count in col.top_values[:3]
            ) if col.top_values else "–"
            items = [
                col.name,
                str(col.count),
                f"{col.missing_pct}%",
                str(col.unique),
                top_str,
            ]
            for c, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                if 1 <= c <= 3:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                table.setItem(row, c, item)

        return table

    @staticmethod
    def _fmt(val) -> str:
        """Formatiert einen optionalen Float-Wert für die Anzeige."""
        if val is None:
            return "–"
        if isinstance(val, float):
            if abs(val) >= 1000:
                return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return f"{val:.4g}"
        return str(val)
