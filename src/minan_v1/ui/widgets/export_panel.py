"""Export-Panel: Export der aktiven Arbeitsansicht und des HTML-Berichts."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from minan_v1.domain.session_state import SessionState
from minan_v1.resources import default_csv_export_path, default_report_path
from minan_v1.services.export_service import export_csv
from minan_v1.services.report_service import build_report_filename, export_html_report
from minan_v1.ui.dialogs import save_csv_dialog, save_html_dialog


class ExportPanel(QWidget):
    """Panel fuer Export der aktiven Arbeitsansicht."""

    def __init__(self, session: SessionState, parent=None) -> None:
        super().__init__(parent)
        self._session = session
        self._main_window = None
        self._init_ui()

    def set_main_window(self, main_window) -> None:
        self._main_window = main_window

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self._placeholder = QLabel("CSV-Datei laden, um Export zu sehen.")
        self._placeholder.setObjectName("sectionHintLabel")
        self._placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._placeholder)

        self._export_area = QWidget()
        export_layout = QVBoxLayout(self._export_area)

        info_group = QGroupBox("Export-Informationen")
        info_layout = QVBoxLayout()
        self._info_label = QLabel("Keine Daten zum Export.")
        self._info_label.setWordWrap(True)
        info_layout.addWidget(self._info_label)
        info_group.setLayout(info_layout)
        export_layout.addWidget(info_group)

        csv_group = QGroupBox("CSV-Weitergabe")
        csv_layout = QVBoxLayout()
        self._exclude_hidden_btn = QPushButton(
            "✓ Ausgeblendete Spalten nicht exportieren"
        )
        self._exclude_hidden_btn.setCheckable(True)
        self._exclude_hidden_btn.setChecked(True)
        self._exclude_hidden_btn.setMinimumHeight(40)
        self._exclude_hidden_btn.setStyleSheet(
            "QPushButton { text-align: left; padding-left: 12px; }"
            "QPushButton:checked { background-color: #2e7d32; color: white; font-weight: bold; }"
            "QPushButton:!checked { background-color: #f5f5f5; color: #666; }"
        )
        csv_layout.addWidget(self._exclude_hidden_btn)
        csv_hint = QLabel(
            "Standardziel: output/csv im sichtbaren Hauptordner der Anwendung."
        )
        csv_hint.setWordWrap(True)
        csv_layout.addWidget(csv_hint)

        csv_btn = QPushButton("Aktive Sicht als CSV exportieren...")
        csv_btn.clicked.connect(self._on_export_csv)
        csv_layout.addWidget(csv_btn)
        csv_group.setLayout(csv_layout)
        export_layout.addWidget(csv_group)

        report_group = QGroupBox("Analysebericht")
        report_layout = QVBoxLayout()
        report_hint = QLabel(
            "Erzeugt einen lokalen HTML-Bericht aus der aktuellen aktiven Sicht. "
            "Standardziel ist output/reports im Hauptordner der Anwendung."
        )
        report_hint.setWordWrap(True)
        report_layout.addWidget(report_hint)

        report_btn = QPushButton("HTML-Bericht exportieren...")
        report_btn.clicked.connect(self._on_export_report)
        report_layout.addWidget(report_btn)
        report_group.setLayout(report_layout)
        export_layout.addWidget(report_group)

        self._status_label = QLabel("")
        self._status_label.setObjectName("panelStatusLabel")
        self._status_label.setWordWrap(True)
        export_layout.addWidget(self._status_label)

        export_layout.addStretch()
        self._export_area.hide()
        layout.addWidget(self._export_area)

    def update_export_info(self) -> None:
        self._placeholder.hide()
        self._export_area.show()

        if not self._session.has_data:
            self._info_label.setText("Keine Daten zum Export.")
            return

        df = self._session.current_df
        hidden_cols = self._session.hidden_columns
        info_lines = [
            f"Aktive Ansicht: {self._session.describe_active_view()}",
            f"Datei: {self._session.import_result.file_name if self._session.import_result else '-'}",
            f"Zeilen in aktiver Ansicht: {len(df)}",
            f"Spalten gesamt: {len(df.columns)}",
            "Standardordner Berichte: output/reports",
            "Standardordner CSV: output/csv",
        ]
        if hidden_cols:
            visible_cols = len(df.columns) - len(
                [col for col in hidden_cols if col in df.columns]
            )
            info_lines.append(f"Ausgeblendete Spalten: {len(hidden_cols)}")
            info_lines.append(f"Sichtbar fuer Tabelle/CSV: {visible_cols}")
        if self._session.last_report and self._session.last_report.file_path:
            info_lines.append(
                f"Letzter Bericht: {self._session.last_report.file_path.name}"
            )
        if self._session.last_export and self._session.last_export.file_path:
            info_lines.append(
                f"Letzter CSV-Export: {self._session.last_export.file_path.name}"
            )

        self._info_label.setText("\n".join(info_lines))

    def _on_export_csv(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten zum Export.")
            return

        file_name = f"{self._session.import_result.file_name.rsplit('.', 1)[0]}_aktive_sicht.csv"
        target_path = save_csv_dialog(self, str(default_csv_export_path(file_name)))
        if target_path is None:
            return

        if self._session.source_path and target_path == self._session.source_path:
            self._show_error(
                "Die Originaldatei darf nicht ueberschrieben werden. Bitte einen anderen Dateinamen waehlen."
            )
            return

        hidden_columns = (
            self._session.hidden_columns if self._exclude_hidden_btn.isChecked() else []
        )
        result = export_csv(
            self._session.current_df, target_path, hidden_columns=hidden_columns
        )
        if result.success:
            self._session.last_export = result
            self._update_status(
                "CSV-Export erfolgreich!\n"
                f"Datei: {result.file_path}\n"
                f"Zeilen: {result.row_count}\n"
                f"Spalten: {result.column_count}"
            )
            self.update_export_info()
        else:
            self._show_error(f"Export fehlgeschlagen:\n{result.error}")

    def _on_export_report(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten fuer einen Bericht vorhanden.")
            return

        target_path = save_html_dialog(
            self, str(default_report_path(build_report_filename()))
        )
        if target_path is None:
            return

        result = export_html_report(self._session, target_path)
        if result.success:
            self._session.last_report = result
            self._update_status(
                "HTML-Bericht erfolgreich!\n"
                f"Datei: {result.file_path}\n"
                f"Sicht: {result.view_name}\n"
                f"Zeilen: {result.row_count}\n"
                f"Spalten: {result.column_count}"
            )
            self.update_export_info()
        else:
            self._show_error(f"Bericht fehlgeschlagen:\n{result.error}")

    def _update_status(self, message: str) -> None:
        self._status_label.setText(message)

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Fehler", message)
