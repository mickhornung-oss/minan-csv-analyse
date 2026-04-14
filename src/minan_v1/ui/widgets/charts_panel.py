"""Diagramm-Panel: Zeigt Standarddiagramme mit Typ-/Spaltenauswahl."""

import logging
from typing import Optional

import matplotlib
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from minan_v1.domain.models import DatasetProfile
from minan_v1.services.chart_service import (
    create_bar_chart,
    create_boxplot,
    create_correlation_heatmap,
    create_histogram,
    create_missing_chart,
    get_categorical_columns,
    get_numeric_columns,
)

matplotlib.use("Agg")

CHART_TYPES = [
    ("Fehlwerte", "missing"),
    ("Histogramm", "histogram"),
    ("Boxplot", "boxplot"),
    ("Top-Kategorien", "bar"),
    ("Korrelation", "correlation"),
]


class ChartsPanel(QWidget):
    """Panel fuer interaktive Diagramm-Auswahl und -Anzeige."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._logger = logging.getLogger(__name__)
        self._df: Optional[pd.DataFrame] = None
        self._profile: Optional[DatasetProfile] = None
        self._current_canvas: Optional[FigureCanvas] = None
        self._last_error_message: Optional[str] = None
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        controls = QHBoxLayout()
        controls.setSpacing(8)

        controls.addWidget(QLabel("Diagrammtyp:"))
        self._type_combo = QComboBox()
        for label, _ in CHART_TYPES:
            self._type_combo.addItem(label)
        self._type_combo.currentIndexChanged.connect(self._on_type_changed)
        controls.addWidget(self._type_combo)

        controls.addWidget(QLabel("Spalte:"))
        self._col_combo = QComboBox()
        self._col_combo.currentIndexChanged.connect(self._on_draw)
        controls.addWidget(self._col_combo)

        controls.addStretch()
        layout.addLayout(controls)

        self._chart_area = QVBoxLayout()
        self._placeholder = QLabel("CSV-Datei laden, um Diagramme zu sehen.")
        self._placeholder.setObjectName("sectionHintLabel")
        self._placeholder.setAlignment(Qt.AlignCenter)
        self._chart_area.addWidget(self._placeholder)
        layout.addLayout(self._chart_area)

    def set_data(self, df: pd.DataFrame, profile: DatasetProfile) -> None:
        """Setzt den DataFrame und das Profil fuer die Diagramme."""
        self._df = df
        self._profile = profile
        self._placeholder.hide()
        self._on_type_changed()

    def _on_type_changed(self, _index: int = 0) -> None:
        """Aktualisiert die Spaltenauswahl basierend auf dem Diagrammtyp."""
        if self._profile is None:
            return

        chart_id = CHART_TYPES[self._type_combo.currentIndex()][1]
        self._col_combo.blockSignals(True)
        self._col_combo.clear()

        if chart_id in ("histogram", "boxplot"):
            cols = get_numeric_columns(self._profile)
            if cols:
                self._col_combo.addItems(cols)
            else:
                self._col_combo.addItem("(keine numerischen Spalten)")
            self._col_combo.setEnabled(bool(cols))
        elif chart_id == "bar":
            cols = get_categorical_columns(self._profile)
            if cols:
                self._col_combo.addItems(cols)
            else:
                self._col_combo.addItem("(keine kategorialen Spalten)")
            self._col_combo.setEnabled(bool(cols))
        else:
            self._col_combo.addItem("(alle Spalten)")
            self._col_combo.setEnabled(False)

        self._col_combo.blockSignals(False)
        self._on_draw()

    def _on_draw(self) -> None:
        """Erzeugt und zeigt das ausgewaehlte Diagramm."""
        if self._df is None or self._profile is None:
            return

        chart_id = CHART_TYPES[self._type_combo.currentIndex()][1]
        col_name = self._col_combo.currentText()
        self._last_error_message = None
        fig = self._create_figure(chart_id, col_name)
        self._show_figure(fig)

    def _create_figure(self, chart_id: str, col_name: str) -> Optional[Figure]:
        """Erzeugt die Figure basierend auf Typ und Spalte."""
        try:
            if chart_id == "missing":
                return create_missing_chart(self._df)
            if chart_id == "histogram" and col_name in self._df.columns:
                return create_histogram(self._df, col_name)
            if chart_id == "boxplot" and col_name in self._df.columns:
                return create_boxplot(self._df, col_name)
            if chart_id == "bar" and col_name in self._df.columns:
                return create_bar_chart(self._df, col_name)
            if chart_id == "correlation":
                return create_correlation_heatmap(self._df)
        except (ValueError, TypeError, KeyError) as exc:
            self._last_error_message = f"Diagramm konnte nicht erstellt werden: {exc}"
            self._logger.exception("Chart rendering failed for %s/%s", chart_id, col_name)
            return None
        return None

    def _show_figure(self, fig: Optional[Figure]) -> None:
        """Zeigt eine Figure im Chart-Bereich oder eine Hinweis-Meldung."""
        if self._current_canvas is not None:
            self._chart_area.removeWidget(self._current_canvas)
            self._current_canvas.setParent(None)
            self._current_canvas.figure.clear()
            self._current_canvas.close()
            self._current_canvas = None

        for i in reversed(range(self._chart_area.count())):
            item = self._chart_area.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, QLabel) and widget is not self._placeholder:
                self._chart_area.removeWidget(widget)
                widget.deleteLater()

        if fig is None:
            hint = QLabel(self._last_error_message or "Fuer diese Auswahl ist kein Diagramm verfuegbar.")
            hint.setObjectName("sectionHintLabel")
            hint.setAlignment(Qt.AlignCenter)
            self._chart_area.addWidget(hint)
            return

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._chart_area.addWidget(canvas)
        self._current_canvas = canvas
        canvas.draw()
