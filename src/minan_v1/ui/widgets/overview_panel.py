"""Überblick-Panel: Zeigt Erstüberblick nach CSV-Import."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGroupBox,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from minan_v1.domain.models import (
    DatasetProfile,
    ImportResult,
    QualityReport,
    SummaryResult,
)
from minan_v1.utils.file_helpers import file_size_readable


class OverviewPanel(QWidget):
    """Panel für den Erstüberblick nach dem CSV-Import."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Scroll-Bereich für den Inhalt
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(12, 12, 12, 12)
        self._content_layout.setSpacing(10)
        self._content_layout.setAlignment(Qt.AlignTop)

        # Platzhalter-Label
        self._placeholder = QLabel("CSV-Datei laden, um den Überblick zu sehen.")
        self._placeholder.setObjectName("sectionHintLabel")
        self._content_layout.addWidget(self._placeholder)

        scroll.setWidget(self._content)
        layout.addWidget(scroll)

    def update_overview(
        self,
        import_result: ImportResult,
        profile: DatasetProfile,
        quality: QualityReport,
        summary: SummaryResult,
    ) -> None:
        """Aktualisiert das Panel mit den Analyseergebnissen."""
        # Altes Layout leeren
        self._clear_content()

        # --- Dateiinfo ---
        file_box = self._create_group("Datei")
        self._add_info(file_box, "Dateiname", import_result.file_name)
        self._add_info(
            file_box, "Quelle", self._format_source_hint(import_result.file_path)
        )
        self._add_info(file_box, "Encoding", import_result.encoding)
        self._add_info(file_box, "Trennzeichen", repr(import_result.separator))
        if profile.file_size_bytes > 0:
            self._add_info(
                file_box, "Dateigröße", file_size_readable(profile.file_size_bytes)
            )
        self._content_layout.addWidget(file_box)

        # --- Struktur ---
        struct_box = self._create_group("Struktur")
        self._add_info(struct_box, "Zeilen", str(profile.row_count))
        self._add_info(struct_box, "Spalten", str(profile.column_count))
        self._add_info(struct_box, "Numerisch", str(profile.numeric_columns))
        self._add_info(struct_box, "Kategorisch", str(profile.categorical_columns))
        if profile.datetime_columns > 0:
            self._add_info(struct_box, "Datum", str(profile.datetime_columns))
        if profile.id_columns > 0:
            self._add_info(struct_box, "ID-Spalten", str(profile.id_columns))
        if profile.text_columns > 0:
            self._add_info(struct_box, "Text", str(profile.text_columns))
        if profile.unknown_columns > 0:
            self._add_info(struct_box, "Unbekannt", str(profile.unknown_columns))
        self._content_layout.addWidget(struct_box)

        # --- Qualität ---
        qual_box = self._create_group("Datenqualität")
        self._add_info(qual_box, "Fehlende Werte gesamt", str(profile.total_missing))
        self._add_info(qual_box, "Doppelte Zeilen", str(quality.duplicate_rows))
        if quality.empty_columns:
            self._add_info(qual_box, "Leere Spalten", ", ".join(quality.empty_columns))
        if quality.constant_columns:
            self._add_info(
                qual_box, "Konstante Spalten", ", ".join(quality.constant_columns)
            )
        self._content_layout.addWidget(qual_box)

        # --- Auffälligkeiten ---
        if quality.findings:
            # Trenne Warnungen und Hinweise
            warnings = [
                f for f in quality.findings if f.severity in ["critical", "warning"]
            ]
            hints = [f for f in quality.findings if f.severity == "info"]

            if warnings:
                warnings_box = self._create_group("Warnungen")
                for finding in warnings:
                    icon = {"critical": "\u2716", "warning": "\u26A0"}.get(
                        finding.severity, ""
                    )
                    label = QLabel(f"{icon} {finding.message}")
                    label.setWordWrap(True)
                    if finding.severity == "critical":
                        label.setStyleSheet("color: #d32f2f;")
                    elif finding.severity == "warning":
                        label.setStyleSheet("color: #f57c00;")
                    warnings_box.layout().addWidget(label)
                self._content_layout.addWidget(warnings_box)

            if hints:
                hints_box = self._create_group("Hinweise")
                for finding in hints:
                    label = QLabel(f"\u2139 {finding.message}")
                    label.setWordWrap(True)
                    label.setStyleSheet("color: #1976d2;")
                    hints_box.layout().addWidget(label)
                self._content_layout.addWidget(hints_box)

        # --- Zusammenfassung ---
        summary_box = self._create_group("Zusammenfassung")
        summary_label = QLabel(summary.text)
        summary_label.setWordWrap(True)
        summary_label.setStyleSheet("font-size: 13px; line-height: 1.5;")
        summary_box.layout().addWidget(summary_label)
        self._content_layout.addWidget(summary_box)

        # Import-Warnungen
        if import_result.warnings:
            warn_box = self._create_group("Import-Hinweise")
            for w in import_result.warnings:
                warn_box.layout().addWidget(QLabel(f"\u26A0 {w}"))
            self._content_layout.addWidget(warn_box)

        self._content_layout.addStretch()

    def _clear_content(self) -> None:
        """Entfernt alle Widgets aus dem Content-Layout."""
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _create_group(self, title: str) -> QGroupBox:
        box = QGroupBox(title)
        box.setLayout(QVBoxLayout())
        return box

    def _add_info(self, group: QGroupBox, label: str, value: str) -> None:
        row = QLabel(f"<b>{label}:</b> {value}")
        row.setTextFormat(Qt.RichText)
        group.layout().addWidget(row)

    def _format_source_hint(self, path) -> str:
        if path is None:
            return "Unbekannte Quelle"

        parts = [part.lower() for part in path.parts]
        if "sample_data" in parts:
            return f"Mitgelieferte Beispieldatei ({path.name})"
        return f"Lokal gewaehlte Datei ({path.name})"
