"""Hauptfenster der MinAn 1.4 Anwendung."""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QMenu,
    QMenuBar,
    QStatusBar,
    QTabWidget,
    QToolBar,
)

from minan_v1.config import APP_TITLE, APP_VERSION, SAMPLE_FILE_NAME
from minan_v1.domain.enums import AnalysisStatus
from minan_v1.domain.session_state import SessionState
from minan_v1.resources import (
    default_report_path,
    ensure_runtime_dirs,
    icon_path,
    sample_data_path,
)
from minan_v1.services.import_service import load_csv
from minan_v1.services.profile_service import create_profile
from minan_v1.services.quality_service import compute_quality_report
from minan_v1.services.report_service import build_report_filename, export_html_report
from minan_v1.services.summary_service import generate_summary
from minan_v1.ui.dialogs import (
    open_csv_dialog,
    save_html_dialog,
    show_error,
    show_info,
    show_quickstart_dialog,
)
from minan_v1.ui.widgets.charts_panel import ChartsPanel
from minan_v1.ui.widgets.edit_panel import EditPanel
from minan_v1.ui.widgets.export_panel import ExportPanel
from minan_v1.ui.widgets.metrics_panel import MetricsPanel
from minan_v1.ui.widgets.overview_panel import OverviewPanel
from minan_v1.ui.widgets.table_panel import TablePanel


class MainWindow(QMainWindow):
    """Zentrales Anwendungsfenster mit Tab-basierter Navigation."""

    def __init__(self, session: SessionState, parent=None) -> None:
        super().__init__(parent)
        self._session = session
        ensure_runtime_dirs()
        self._init_ui()

    def _init_ui(self) -> None:
        self.setObjectName("mainWindow")
        self.setWindowTitle(APP_TITLE)
        app_icon = icon_path("minan_v1.ico")
        if app_icon.exists():
            self.setWindowIcon(QIcon(str(app_icon)))
        self._menu_bar = QMenuBar(self)
        self.setMenuBar(self._menu_bar)
        self._setup_menus()
        self._setup_toolbar()

        self._tabs = QTabWidget(self)
        self._tabs.setDocumentMode(False)
        self.setCentralWidget(self._tabs)

        self._overview_panel = OverviewPanel()
        self._table_panel = TablePanel()
        self._metrics_panel = MetricsPanel()
        self._charts_panel = ChartsPanel()
        self._edit_panel = EditPanel(self._session)
        self._edit_panel.set_main_window(self)
        self._export_panel = ExportPanel(self._session)
        self._export_panel.set_main_window(self)

        self._tabs.addTab(self._overview_panel, "Ueberblick")
        self._tabs.addTab(self._table_panel, "Tabelle")
        self._tabs.addTab(self._metrics_panel, "Kennzahlen")
        self._tabs.addTab(self._charts_panel, "Diagramme")
        self._tabs.addTab(self._edit_panel, "Bearbeiten")
        self._tabs.addTab(self._export_panel, "Export")

        self._status_bar = QStatusBar(self)
        self.setStatusBar(self._status_bar)
        self._status_bar.showMessage(
            f"Bereit - CSV-Datei laden oder Info / Schnellstart oeffnen. Version {APP_VERSION}"
        )
        self._apply_window_style()

    def _setup_menus(self) -> None:
        file_menu: QMenu = self._menu_bar.addMenu("&Datei")

        open_action = QAction("CSV &oeffnen...", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self._on_open_csv)
        file_menu.addAction(open_action)

        report_action = QAction("&Bericht exportieren...", self)
        report_action.setShortcut(QKeySequence("Ctrl+Shift+E"))
        report_action.triggered.connect(self._on_export_report)
        file_menu.addAction(report_action)

        file_menu.addSeparator()

        quit_action = QAction("&Beenden", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        info_menu: QMenu = self._menu_bar.addMenu("&Info")
        quickstart_action = QAction("&Info / Schnellstart", self)
        quickstart_action.setShortcut(QKeySequence("F1"))
        quickstart_action.triggered.connect(self.show_quickstart)
        info_menu.addAction(quickstart_action)

    def _setup_toolbar(self) -> None:
        toolbar = QToolBar("Schnellzugriff", self)
        toolbar.setMovable(False)
        toolbar.setObjectName("mainToolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.addToolBar(toolbar)

        open_action = QAction("CSV oeffnen", self)
        open_action.triggered.connect(self._on_open_csv)
        toolbar.addAction(open_action)

        report_action = QAction("Bericht exportieren", self)
        report_action.triggered.connect(self._on_export_report)
        toolbar.addAction(report_action)

        quickstart_action = QAction("Info / Schnellstart", self)
        quickstart_action.triggered.connect(self.show_quickstart)
        toolbar.addAction(quickstart_action)

        toolbar.widgetForAction(open_action).setProperty("toolbarRole", "primary")
        toolbar.widgetForAction(report_action).setProperty("toolbarRole", "primary")
        toolbar.widgetForAction(quickstart_action).setProperty(
            "toolbarRole", "secondary"
        )
        toolbar.style().unpolish(toolbar)
        toolbar.style().polish(toolbar)

    def _apply_window_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow#mainWindow {
                background: #141918;
            }
            QMenuBar {
                background: #1a211f;
                color: #dce8e1;
                border-bottom: 1px solid #28312e;
                padding: 4px 8px;
            }
            QMenuBar::item {
                padding: 6px 10px;
                border-radius: 6px;
                background: transparent;
            }
            QMenuBar::item:selected {
                background: #27312d;
            }
            QMenu {
                background: #202725;
                color: #e3ece7;
                border: 1px solid #2d3734;
                padding: 6px;
            }
            QMenu::item {
                padding: 7px 22px 7px 10px;
                border-radius: 6px;
            }
            QMenu::item:selected {
                background: #2a3631;
            }
            QToolBar#mainToolbar {
                background: #181f1d;
                border: none;
                border-bottom: 1px solid #28312e;
                padding: 10px 14px 8px 14px;
                spacing: 8px;
            }
            QToolBar#mainToolbar QToolButton {
                background: #202826;
                color: #dce8e1;
                border: 1px solid #303936;
                border-radius: 10px;
                padding: 8px 14px;
                margin-right: 4px;
                font-weight: 600;
            }
            QToolBar#mainToolbar QToolButton:hover {
                background: #27312e;
                border-color: #416f59;
            }
            QToolBar#mainToolbar QToolButton[toolbarRole="primary"] {
                background: #1f2f28;
                border-color: #4c936c;
                color: #edf6f0;
            }
            QToolBar#mainToolbar QToolButton[toolbarRole="primary"]:hover {
                background: #254035;
                border-color: #58a276;
            }
            QTabWidget::pane {
                border: 1px solid #2a3230;
                background: #1b2220;
                border-radius: 14px;
                top: -1px;
                padding: 8px;
            }
            QTabBar::tab {
                background: #1b2321;
                color: #90a79b;
                border: 1px solid #2e3734;
                border-bottom: none;
                padding: 9px 16px;
                margin-right: 4px;
                min-width: 104px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: #22322b;
                color: #ecf6ef;
                border-color: #4e9b70;
            }
            QTabBar::tab:hover:!selected {
                background: #202927;
                color: #cad9d1;
            }
            QWidget {
                color: #d8e5dd;
            }
            QGroupBox {
                background: #202725;
                border: 1px solid #303937;
                border-radius: 14px;
                margin-top: 14px;
                padding: 12px 12px 12px 12px;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
                color: #e3eee7;
            }
            QLabel {
                color: #d7e4dd;
            }
            QLabel#sectionHintLabel {
                color: #94aba0;
                background: #18201d;
                border: 1px solid #2b3431;
                border-radius: 8px;
                padding: 10px 12px;
            }
            QLabel#panelStatusLabel {
                color: #b2c3ba;
                background: #181f1d;
                border: 1px dashed #33403a;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel#filtersCaptionLabel {
                color: #9fb1a7;
                font-size: 12px;
                font-weight: 600;
                padding: 0 2px;
            }
            QListWidget#activeFiltersList {
                background: #141918;
                border: 1px solid #2e3734;
                border-radius: 8px;
                padding: 2px;
                outline: none;
            }
            QLineEdit, QComboBox, QListWidget {
                background: #171d1c;
                color: #ecf4ef;
                border: 1px solid #303a36;
                border-radius: 8px;
                padding: 6px 10px;
                min-height: 18px;
            }
            QLineEdit:focus, QComboBox:focus, QListWidget:focus {
                border: 1px solid #54a372;
                background: #1c2422;
            }
            QComboBox {
                padding-right: 34px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border-left: 1px solid #36413d;
                background: #202826;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QComboBox::down-arrow {
                width: 0px;
                height: 0px;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #b8c9c0;
                margin-right: 8px;
            }
            QPushButton {
                background: #262e2c;
                color: #dfe9e3;
                border: 1px solid #333d39;
                border-radius: 8px;
                padding: 7px 12px;
                font-weight: 600;
                min-height: 18px;
            }
            QPushButton:hover {
                background: #2b3532;
                border-color: #48695a;
            }
            QPushButton:pressed {
                background: #1f2926;
            }
            QPushButton#primaryActionButton {
                background: #1f392d;
                border-color: #56a374;
                color: #f0f8f3;
            }
            QPushButton#primaryActionButton:hover {
                background: #254637;
                border-color: #63b07f;
            }
            QPushButton#secondaryActionButton {
                background: #232b29;
            }
            QPushButton#secondaryActionButton:hover {
                border-color: #55645d;
            }
            QPushButton#toggleActionButton {
                background: #202826;
                border: 1px solid #3a4541;
                color: #c9d6cf;
                text-align: left;
                padding-left: 12px;
            }
            QPushButton#toggleActionButton:hover {
                border-color: #587364;
            }
            QPushButton#toggleActionButton:checked {
                background: #244235;
                border-color: #56a374;
                color: #eff8f2;
            }
            QPushButton:checked {
                background: #244235;
                border-color: #56a374;
            }
            QRadioButton {
                spacing: 6px;
            }
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
            }
            QRadioButton::indicator:unchecked {
                border: 1px solid #4a5751;
                border-radius: 7px;
                background: #161c1a;
            }
            QRadioButton::indicator:checked {
                border: 1px solid #56a374;
                border-radius: 7px;
                background: #56a374;
            }
            QScrollArea, QTableView, QTableWidget {
                background: #1a201f;
                alternate-background-color: #1f2725;
                border: 1px solid #2f3836;
                border-radius: 10px;
                gridline-color: #2b3331;
                color: #e6efe9;
                selection-background-color: #294337;
                selection-color: #f4faf6;
            }
            QHeaderView::section {
                background: #242c2a;
                color: #cdd8d2;
                border: none;
                border-right: 1px solid #303937;
                border-bottom: 1px solid #303937;
                padding: 7px 8px;
                font-weight: 600;
            }
            QStatusBar {
                background: #181f1d;
                color: #d5e1da;
                border-top: 1px solid #28312e;
            }
            """
        )

    def _on_open_csv(self) -> None:
        path = open_csv_dialog(self)
        if path is None:
            return
        self.load_csv_path(path)

    def show_quickstart(self) -> bool:
        """Oeffnet den Schnellstart-Dialog und laedt optional die Beispieldatei."""
        should_load_sample = show_quickstart_dialog(self)
        if should_load_sample:
            return self.load_sample_dataset()
        return False

    def load_sample_dataset(self) -> bool:
        """Laedt die mitgelieferte Beispieldatei."""
        path = sample_data_path(SAMPLE_FILE_NAME)
        if not path.exists():
            show_error(
                self,
                "Beispieldatei fehlt",
                "Die mitgelieferte Beispieldatei konnte nicht gefunden werden.",
            )
            return False
        ok = self.load_csv_path(path)
        if ok:
            self._tabs.setCurrentIndex(0)
            self._status_bar.showMessage(f"Beispieldatei geladen - {path.name}")
        return ok

    def load_csv_path(self, path: Path) -> bool:
        """Laedt eine CSV-Datei direkt ueber einen Pfad."""
        self._status_bar.showMessage(f"Lade {path.name}...")
        df, import_result = load_csv(path)
        if not import_result.success:
            show_error(self, "Import-Fehler", import_result.error)
            self._status_bar.showMessage("Import fehlgeschlagen.")
            return False

        self._session.load(df, path)
        self._session.import_result = import_result

        try:
            self._recompute_analysis()
            self._session.status = AnalysisStatus.ANALYZED
        except Exception as exc:
            show_error(self, "Analysefehler", f"Fehler bei der Analyse:\n{exc}")
            self._status_bar.showMessage("Analyse fehlgeschlagen.")
            return False

        self._refresh_panels()
        self._status_bar.showMessage(
            f"{import_result.file_name} geladen - "
            f"{self._session.profile.row_count} Zeilen, {self._session.profile.column_count} Spalten"
        )
        self._tabs.setCurrentIndex(0)
        return True

    def _on_export_report(self) -> None:
        if not self._session.has_data:
            show_error(
                self, "Kein Bericht moeglich", "Bitte zuerst eine CSV-Datei laden."
            )
            return

        default_path = str(default_report_path(build_report_filename()))
        target_path = save_html_dialog(self, default_path)
        if target_path is None:
            return

        result = self.export_report_to_path(target_path)
        if result.success:
            show_info(
                self,
                "Bericht erstellt",
                f"HTML-Bericht gespeichert:\n{result.file_path}\n\n"
                f"Sicht: {result.view_name}\n"
                f"Zeilen: {result.row_count}\nSpalten: {result.column_count}",
            )
        else:
            show_error(self, "Bericht fehlgeschlagen", result.error)

    def export_report_to_path(self, target_path: Path):
        """Exportiert den HTML-Bericht direkt an einen Zielpfad."""
        result = export_html_report(self._session, target_path)
        if result.success:
            self._session.last_report = result
            self._status_bar.showMessage(
                f"Bericht exportiert - {result.file_path.name} ({result.view_name})"
            )
        return result

    def _refresh_after_edit(self) -> None:
        if not self._session.has_data:
            return

        self._recompute_analysis()
        self._refresh_panels()

        visible_df = self._session.current_df
        view_text = self._session.describe_active_view()
        self._status_bar.showMessage(
            f"Arbeitsansicht aktualisiert - {len(visible_df)} Zeilen, "
            f"{len(visible_df.columns)} Spalten | {view_text}"
        )

    def _recompute_analysis(self) -> None:
        visible_df = self._session.current_df
        profile = create_profile(visible_df, self._session.manual_column_types)
        profile.source_path = self._session.source_path
        if self._session.import_result:
            import_result = self._session.import_result
            profile.file_size_bytes = (
                import_result.file_path.stat().st_size if import_result.file_path else 0
            )
            profile.encoding_detected = import_result.encoding
            profile.separator_detected = import_result.separator
        self._session.profile = profile
        self._session.quality_report = compute_quality_report(visible_df, profile)
        self._session.summary = generate_summary(profile, self._session.quality_report)

    def _refresh_panels(self) -> None:
        visible_df = self._session.current_df
        self._edit_panel.update_columns(self._session.working_df.columns.tolist())
        self._edit_panel.refresh_view_state()

        duplicate_indices = []
        missing_cells: list[tuple[int, str]] = []
        if self._session.duplicate_marking:
            duplicate_indices = self._session.duplicate_marking.marked_rows
        if self._session.missing_marking:
            missing_cells = self._session.missing_marking.marked_cells

        self._overview_panel.update_overview(
            self._session.import_result,
            self._session.profile,
            self._session.quality_report,
            self._session.summary,
        )
        self._table_panel.set_dataframe(
            visible_df,
            self._session.hidden_columns,
            duplicate_indices,
            missing_cells,
            show_duplicate_marking=self._session.duplicate_marking is not None,
            show_missing_marking=self._session.missing_marking is not None,
        )
        self._metrics_panel.update_metrics(self._session.profile)
        self._charts_panel.set_data(visible_df, self._session.profile)
        self._export_panel.update_export_info()
