"""Dialogfenster fuer Datei-Auswahl, Schnellstart und Meldungen."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def open_csv_dialog(parent: Optional[QWidget] = None) -> Optional[Path]:
    path, _ = QFileDialog.getOpenFileName(
        parent,
        "CSV-Datei oeffnen",
        "",
        "CSV-Dateien (*.csv);;Alle Dateien (*)",
    )
    return Path(path) if path else None


def save_csv_dialog(parent: Optional[QWidget] = None, default_path: str = "") -> Optional[Path]:
    path, _ = QFileDialog.getSaveFileName(
        parent,
        "CSV-Datei speichern",
        default_path,
        "CSV-Dateien (*.csv);;Alle Dateien (*)",
    )
    return Path(path) if path else None


def save_html_dialog(parent: Optional[QWidget] = None, default_path: str = "") -> Optional[Path]:
    path, _ = QFileDialog.getSaveFileName(
        parent,
        "HTML-Bericht speichern",
        default_path,
        "HTML-Dateien (*.html);;Alle Dateien (*)",
    )
    return Path(path) if path else None


class QuickStartDialog(QDialog):
    """Kompakter Schnellstart-Dialog mit Beispiel-Datei-Zugriff."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._load_sample_requested = False
        self.setWindowTitle("Info / Schnellstart")
        self.setMinimumWidth(420)
        self._init_ui()

    @property
    def load_sample_requested(self) -> bool:
        return self._load_sample_requested

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        intro = QLabel(
            "MinAn 1.4 analysiert CSV-Dateien lokal und zeigt Struktur, Datenqualitaet, "
            "Kennzahlen, Diagramme sowie Exportmoeglichkeiten in einer kompakten Oberflaeche."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        steps = QLabel(
            "Schnellstart:\n"
            "1. Eigene CSV oeffnen oder Beispieldatei laden\n"
            "2. Ueberblick und Kennzahlen pruefen\n"
            "3. Bei Bedarf filtern oder Schnellansichten nutzen\n"
            "4. Ergebnisse als HTML-Bericht oder CSV exportieren"
        )
        steps.setWordWrap(True)
        layout.addWidget(steps)

        hint = QLabel(
            "Standardziele:\n"
            "- Berichte: output/reports\n"
            "- CSV-Exporte: output/csv"
        )
        hint.setWordWrap(True)
        layout.addWidget(hint)

        load_button = QPushButton("Beispieldatei laden")
        load_button.clicked.connect(self._on_load_sample)
        layout.addWidget(load_button)

        close_button = QPushButton("Schliessen")
        close_button.clicked.connect(self.reject)
        layout.addWidget(close_button)

    def _on_load_sample(self) -> None:
        self._load_sample_requested = True
        self.accept()


def show_quickstart_dialog(parent: Optional[QWidget] = None) -> bool:
    dialog = QuickStartDialog(parent)
    dialog.exec()
    return dialog.load_sample_requested


def show_error(parent: Optional[QWidget], title: str, message: str) -> None:
    QMessageBox.critical(parent, title, message)


def show_warning(parent: Optional[QWidget], title: str, message: str) -> None:
    QMessageBox.warning(parent, title, message)


def show_info(parent: Optional[QWidget], title: str, message: str) -> None:
    QMessageBox.information(parent, title, message)
