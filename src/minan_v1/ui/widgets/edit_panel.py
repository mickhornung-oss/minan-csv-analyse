"""Bearbeitungs-Panel: Einfache Transformationen und Ansichten."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from minan_v1.domain.enums import ColumnType
from minan_v1.domain.models import FilterCondition, FilterOperator, MarkingResult, SortState
from minan_v1.domain.session_state import SessionState
from minan_v1.services.transform_service import (
    apply_filter,
    apply_sort,
    drop_column,
    focus_duplicate_rows,
    focus_missing_rows,
    focus_outlier_candidates,
    mark_duplicates,
    mark_missing,
    rename_column,
)


class EditPanel(QWidget):
    """Panel fuer einfache Bearbeitungen auf der Arbeitskopie."""

    _TWO_COLUMN_BREAKPOINT = 980

    def __init__(self, session: SessionState, parent=None) -> None:
        super().__init__(parent)
        self._session = session
        self._main_window = None
        self._two_column_mode: bool | None = None
        self._init_ui()

    def set_main_window(self, main_window) -> None:
        self._main_window = main_window

    def _configure_action_button(self, button: QPushButton, min_width: int, max_width: int) -> None:
        button.setMinimumWidth(min_width)
        button.setMaximumWidth(max_width)
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self._placeholder = QLabel("CSV-Datei laden, um Bearbeitungen zu sehen.")
        self._placeholder.setObjectName("sectionHintLabel")
        self._placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._placeholder)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QScrollArea.NoFrame)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._edit_area = QWidget()
        self._edit_area_layout = QVBoxLayout(self._edit_area)
        self._edit_area_layout.setContentsMargins(0, 0, 0, 0)
        self._edit_area_layout.setSpacing(10)

        self._content_row = QWidget()
        self._content_row_layout = QHBoxLayout(self._content_row)
        self._content_row_layout.setContentsMargins(0, 0, 0, 0)
        self._content_row_layout.setSpacing(12)

        self._left_column = QWidget()
        self._left_layout = QVBoxLayout(self._left_column)
        self._left_layout.setContentsMargins(0, 0, 0, 0)
        self._left_layout.setSpacing(10)

        self._right_column = QWidget()
        self._right_layout = QVBoxLayout(self._right_column)
        self._right_layout.setContentsMargins(0, 0, 0, 0)
        self._right_layout.setSpacing(10)

        self._single_column = QWidget()
        self._single_layout = QVBoxLayout(self._single_column)
        self._single_layout.setContentsMargins(0, 0, 0, 0)
        self._single_layout.setSpacing(10)
        self._single_column.hide()

        self._content_row_layout.addWidget(self._left_column, 3)
        self._content_row_layout.addWidget(self._right_column, 2)

        self._state_group = QGroupBox("Aktuelle Ansicht")
        state_layout = QVBoxLayout()
        state_layout.setSpacing(6)
        state_layout.setContentsMargins(10, 8, 10, 10)
        self._view_hint_label = QLabel("Gesamtansicht")
        self._view_hint_label.setWordWrap(True)
        self._view_hint_label.setObjectName("viewStateLabel")
        self._view_hint_label.setMinimumHeight(36)
        state_layout.addWidget(self._view_hint_label)

        self._filters_caption_label = QLabel("Aktive Filter")
        self._filters_caption_label.setObjectName("filtersCaptionLabel")
        state_layout.addWidget(self._filters_caption_label)

        self._active_filters_list = QListWidget()
        self._active_filters_list.setObjectName("activeFiltersList")
        self._active_filters_list.setMinimumHeight(52)
        self._active_filters_list.setMaximumHeight(76)
        state_layout.addWidget(self._active_filters_list)

        state_btns = QHBoxLayout()
        state_btns.setSpacing(8)
        remove_filter_btn = QPushButton("Filter entfernen")
        remove_filter_btn.setObjectName("secondaryActionButton")
        self._configure_action_button(remove_filter_btn, 120, 170)
        remove_filter_btn.clicked.connect(self._on_remove_selected_filter)
        state_btns.addWidget(remove_filter_btn)
        reset_filters_btn = QPushButton("Alle zuruecksetzen")
        reset_filters_btn.setObjectName("secondaryActionButton")
        self._configure_action_button(reset_filters_btn, 130, 185)
        reset_filters_btn.clicked.connect(self._on_reset_filter)
        state_btns.addWidget(reset_filters_btn)

        return_view_btn = QPushButton("Gesamtansicht")
        return_view_btn.setObjectName("primaryActionButton")
        self._configure_action_button(return_view_btn, 130, 185)
        return_view_btn.clicked.connect(self._on_return_to_full_view)
        state_btns.addWidget(return_view_btn)
        state_btns.addStretch()
        state_layout.addLayout(state_btns)
        self._state_group.setLayout(state_layout)

        self._col_group = QGroupBox("Spaltenauswahl")
        col_layout = QVBoxLayout()
        col_layout.setSpacing(8)
        col_layout.setContentsMargins(10, 10, 10, 10)

        column_form = QFormLayout()
        column_form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        column_form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        column_form.setHorizontalSpacing(10)
        column_form.setVerticalSpacing(8)

        self._col_combo = QComboBox()
        self._col_combo.setMinimumWidth(220)
        self._col_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._col_combo.currentIndexChanged.connect(self._on_column_changed)
        column_form.addRow("Spalte:", self._col_combo)

        self._type_combo = QComboBox()
        self._type_combo.addItems(
            ["Automatisch", "Numerisch", "Kategorial", "Datum", "ID", "Text"]
        )
        self._type_combo.setMinimumWidth(220)
        self._type_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        column_form.addRow("Spaltentyp:", self._type_combo)
        col_layout.addLayout(column_form)

        type_btn_layout = QHBoxLayout()
        type_btn_layout.setSpacing(8)
        apply_type_btn = QPushButton("Typ anwenden")
        apply_type_btn.setObjectName("primaryActionButton")
        self._configure_action_button(apply_type_btn, 120, 160)
        apply_type_btn.clicked.connect(self._on_apply_type)
        type_btn_layout.addWidget(apply_type_btn)
        reset_type_btn = QPushButton("Typ zuruecksetzen")
        reset_type_btn.setObjectName("secondaryActionButton")
        self._configure_action_button(reset_type_btn, 135, 185)
        reset_type_btn.clicked.connect(self._on_reset_type)
        type_btn_layout.addWidget(reset_type_btn)
        type_btn_layout.addStretch()
        col_layout.addLayout(type_btn_layout)

        ops_layout = QHBoxLayout()
        ops_layout.setSpacing(10)
        ops_layout.setAlignment(Qt.AlignTop)

        rename_layout = QVBoxLayout()
        rename_layout.setSpacing(6)
        rename_layout.addWidget(QLabel("Umbenennen:"))
        self._new_name_edit = QLineEdit()
        self._new_name_edit.setPlaceholderText("Neuer Spaltenname")
        self._new_name_edit.setMinimumWidth(220)
        self._new_name_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        rename_layout.addWidget(self._new_name_edit)
        rename_btn = QPushButton("Umbenennen")
        rename_btn.setObjectName("secondaryActionButton")
        self._configure_action_button(rename_btn, 120, 150)
        rename_btn.clicked.connect(self._on_rename_column)
        rename_layout.addWidget(rename_btn)
        ops_layout.addLayout(rename_layout)

        drop_layout = QVBoxLayout()
        drop_layout.setSpacing(6)
        drop_btn = QPushButton("Spalte entfernen")
        drop_btn.setObjectName("secondaryActionButton")
        self._configure_action_button(drop_btn, 135, 170)
        drop_btn.clicked.connect(self._on_drop_column)
        drop_layout.addWidget(drop_btn)
        hide_btn = QPushButton("Spalte ausblenden")
        hide_btn.setObjectName("secondaryActionButton")
        self._configure_action_button(hide_btn, 135, 170)
        hide_btn.clicked.connect(self._on_hide_column)
        drop_layout.addWidget(hide_btn)
        unhide_btn = QPushButton("Alle einblenden")
        unhide_btn.setObjectName("secondaryActionButton")
        self._configure_action_button(unhide_btn, 120, 160)
        unhide_btn.clicked.connect(self._on_unhide_all)
        drop_layout.addWidget(unhide_btn)
        ops_layout.addLayout(drop_layout)
        ops_layout.addStretch()

        col_layout.addLayout(ops_layout)
        self._col_group.setLayout(col_layout)

        self._filter_group = QGroupBox("Filter")
        filter_layout = QVBoxLayout()
        filter_layout.setSpacing(8)
        filter_layout.setContentsMargins(10, 10, 10, 10)

        filter_form = QFormLayout()
        filter_form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        filter_form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        filter_form.setHorizontalSpacing(10)
        filter_form.setVerticalSpacing(8)
        self._filter_op_combo = QComboBox()
        self._filter_op_combo.addItems(
            [
                "Gleich",
                "Ungleich",
                "Groesser als",
                "Kleiner als",
                "Zwischen",
                "Enthaelt",
                "Beginnt mit",
                "Ist leer",
                "Ist nicht leer",
            ]
        )
        self._filter_op_combo.currentIndexChanged.connect(self._on_filter_op_changed)
        self._filter_op_combo.setMinimumWidth(220)
        self._filter_op_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filter_form.addRow("Operator:", self._filter_op_combo)

        self._filter_value1_edit = QLineEdit()
        self._filter_value1_edit.setPlaceholderText("Wert")
        self._filter_value1_edit.setMinimumWidth(220)
        self._filter_value1_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filter_form.addRow("Wert:", self._filter_value1_edit)

        self._filter_value2_edit = QLineEdit()
        self._filter_value2_edit.setPlaceholderText("Endwert (fuer Bereich)")
        self._filter_value2_edit.setMinimumWidth(220)
        self._filter_value2_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._filter_value2_edit.setVisible(False)
        filter_form.addRow("Bis:", self._filter_value2_edit)
        filter_layout.addLayout(filter_form)

        apply_filter_btn = QPushButton("Filter hinzufuegen")
        apply_filter_btn.setObjectName("primaryActionButton")
        self._configure_action_button(apply_filter_btn, 130, 175)
        apply_filter_btn.clicked.connect(self._on_apply_filter)
        filter_layout.addWidget(apply_filter_btn)

        self._filter_group.setLayout(filter_layout)

        self._sort_group = QGroupBox("Sortierung")
        sort_layout = QVBoxLayout()
        sort_layout.setSpacing(8)
        sort_layout.setContentsMargins(10, 10, 10, 10)

        sort_dir_layout = QHBoxLayout()
        sort_dir_layout.setSpacing(12)
        sort_dir_layout.setAlignment(Qt.AlignLeft)
        self._sort_asc_radio = QRadioButton("Aufsteigend")
        self._sort_desc_radio = QRadioButton("Absteigend")
        self._sort_asc_radio.setChecked(True)
        self._sort_button_group = QButtonGroup(self)
        self._sort_button_group.addButton(self._sort_asc_radio)
        self._sort_button_group.addButton(self._sort_desc_radio)
        sort_dir_layout.addWidget(self._sort_asc_radio)
        sort_dir_layout.addWidget(self._sort_desc_radio)
        sort_layout.addLayout(sort_dir_layout)

        sort_btn = QPushButton("Sortieren")
        sort_btn.setObjectName("primaryActionButton")
        self._configure_action_button(sort_btn, 110, 140)
        sort_btn.clicked.connect(self._on_sort)
        sort_layout.addWidget(sort_btn)
        self._sort_group.setLayout(sort_layout)

        self._quick_group = QGroupBox("Schnellansichten")
        quick_layout = QVBoxLayout()
        quick_layout.setSpacing(6)
        quick_layout.setContentsMargins(10, 10, 10, 10)
        missing_btn = QPushButton("Fehlende Werte")
        missing_btn.setObjectName("primaryActionButton")
        self._configure_action_button(missing_btn, 140, 185)
        missing_btn.clicked.connect(self._on_focus_missing)
        quick_layout.addWidget(missing_btn)
        duplicates_btn = QPushButton("Dubletten")
        duplicates_btn.setObjectName("primaryActionButton")
        self._configure_action_button(duplicates_btn, 120, 165)
        duplicates_btn.clicked.connect(self._on_focus_duplicates)
        quick_layout.addWidget(duplicates_btn)
        outliers_btn = QPushButton("Ausreisser-Kandidaten")
        outliers_btn.setObjectName("primaryActionButton")
        self._configure_action_button(outliers_btn, 160, 210)
        outliers_btn.clicked.connect(self._on_focus_outliers)
        quick_layout.addWidget(outliers_btn)
        self._quick_group.setLayout(quick_layout)

        self._mark_group = QGroupBox("Markierungen")
        mark_layout = QVBoxLayout()
        mark_layout.setSpacing(6)
        mark_layout.setContentsMargins(10, 10, 10, 10)
        self._mark_duplicates_toggle = QPushButton("Dubletten: EIN")
        self._mark_duplicates_toggle.setObjectName("toggleActionButton")
        self._configure_action_button(self._mark_duplicates_toggle, 150, 190)
        self._mark_duplicates_toggle.setCheckable(True)
        self._mark_duplicates_toggle.setChecked(True)
        self._mark_duplicates_toggle.toggled.connect(self._on_toggle_duplicates)
        mark_layout.addWidget(self._mark_duplicates_toggle)
        self._mark_missing_toggle = QPushButton("Fehlwerte: EIN")
        self._mark_missing_toggle.setObjectName("toggleActionButton")
        self._configure_action_button(self._mark_missing_toggle, 160, 210)
        self._mark_missing_toggle.setCheckable(True)
        self._mark_missing_toggle.setChecked(True)
        self._mark_missing_toggle.toggled.connect(self._on_toggle_missing)
        mark_layout.addWidget(self._mark_missing_toggle)
        self._mark_legend_label = QLabel("Gelb = Fehlwerte, Rot = Dubletten")
        self._mark_legend_label.setObjectName("filtersCaptionLabel")
        mark_layout.addWidget(self._mark_legend_label)
        self._mark_group.setLayout(mark_layout)

        self._status_label = QLabel("")
        self._status_label.setObjectName("panelStatusLabel")
        self._status_label.setWordWrap(True)
        self._status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self._left_groups = [self._col_group, self._filter_group]
        self._right_groups = [self._sort_group, self._quick_group, self._mark_group]

        self._edit_area_layout.addWidget(self._content_row)
        self._edit_area_layout.addWidget(self._single_column)
        self._edit_area_layout.addWidget(self._state_group)
        self._edit_area_layout.addWidget(self._status_label)
        self._edit_area_layout.addStretch()

        self._left_layout.addStretch()
        self._right_layout.addStretch()
        self._single_layout.addStretch()

        self._scroll_area.setWidget(self._edit_area)
        self._edit_area.hide()
        layout.addWidget(self._scroll_area)
        self._scroll_area.hide()

        self._apply_responsive_layout(force=True)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._apply_responsive_layout()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._apply_responsive_layout()

    def update_columns(self, columns: list[str]) -> None:
        """Aktualisiert die Spaltenliste."""
        self._placeholder.hide()
        self._scroll_area.show()
        self._edit_area.show()

        current_text = self._col_combo.currentText()
        self._col_combo.clear()
        self._col_combo.addItems(columns)

        if current_text and current_text in columns:
            self._col_combo.setCurrentIndex(self._col_combo.findText(current_text))

        self._apply_responsive_layout(force=True)
        self.refresh_view_state()

    def refresh_view_state(self) -> None:
        """Aktualisiert Filterliste und Ansichtsstatus."""
        if not self._session.has_data:
            return

        self._sync_markings()
        current_rows = len(self._session.current_df)

        if self._session.has_active_view:
            self._view_hint_label.setText(
                f"{self._session.describe_active_view()} | {current_rows} Zeilen"
            )
            self._view_hint_label.setStyleSheet(
                "font-weight: 600; color: #f2dfaf; background: #2b2418; "
                "border: 1px solid #5b4a28; border-radius: 10px; padding: 6px 10px;"
            )
        else:
            self._view_hint_label.setText(f"Gesamtansicht | {current_rows} Zeilen")
            self._view_hint_label.setStyleSheet(
                "font-weight: 600; color: #caead7; background: #1b2a23; "
                "border: 1px solid #345645; border-radius: 10px; padding: 6px 10px;"
            )

        self._active_filters_list.clear()
        for condition in self._session.active_filters:
            self._active_filters_list.addItem(condition.to_display_text())

        if not self._session.active_filters:
            self._active_filters_list.addItem("(keine aktiven Filter)")
            self._active_filters_list.setCurrentRow(-1)
            self._filters_caption_label.setText("Aktive Filter: keine")
        else:
            self._filters_caption_label.setText(
                f"Aktive Filter: {len(self._session.active_filters)}"
            )
        self._update_mark_toggle_labels()

    def _on_column_changed(self, _index: int) -> None:
        self._type_combo.setCurrentIndex(0)

    def _on_rename_column(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        old_name = self._col_combo.currentText()
        new_name = self._new_name_edit.text().strip()
        if not old_name:
            self._show_error("Keine Spalte ausgewaehlt.")
            return
        if not new_name:
            self._show_error("Kein neuer Name angegeben.")
            return

        result = rename_column(self._session.working_df, old_name, new_name)
        if not result.success or result.df is None:
            self._show_error(result.message)
            return

        self._session.working_df = result.df
        self._rename_view_state_references(old_name, new_name)
        self._new_name_edit.clear()
        self._update_status(result.message)
        self.update_columns(self._session.working_df.columns.tolist())
        self._refresh_main_window()

    def _on_drop_column(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        column = self._col_combo.currentText()
        if not column:
            self._show_error("Keine Spalte ausgewaehlt.")
            return

        result = drop_column(self._session.working_df, column)
        if not result.success or result.df is None:
            self._show_error(result.message)
            return

        self._session.working_df = result.df
        self._remove_view_state_references(column)
        self._update_status(result.message)
        self.update_columns(self._session.working_df.columns.tolist())
        self._refresh_main_window()

    def _on_hide_column(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        column = self._col_combo.currentText()
        if not column:
            self._show_error("Keine Spalte ausgewaehlt.")
            return

        hidden = self._session.hidden_columns.copy()
        if column not in hidden:
            hidden.append(column)
            self._session.hidden_columns = hidden
            self._update_status(f"Spalte '{column}' ausgeblendet.")
            self._refresh_main_window()

    def _on_unhide_all(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        self._session.hidden_columns = []
        self._update_status("Alle Spalten eingeblendet.")
        self._refresh_main_window()

    def _on_filter_op_changed(self, index: int) -> None:
        self._filter_value2_edit.setVisible(index == 4)

    def _on_apply_filter(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        condition = self._build_filter_condition()
        if condition is None:
            return

        result = apply_filter(self._session.current_df, condition)
        if not result.success:
            self._show_error(result.message)
            return

        self._session.add_filter(condition)
        self._filter_value1_edit.clear()
        self._filter_value2_edit.clear()
        self.refresh_view_state()
        self._update_status(f"{condition.to_display_text()} hinzugefuegt.")
        self._refresh_main_window()

    def _on_remove_selected_filter(self) -> None:
        if not self._session.active_filters:
            return

        row = self._active_filters_list.currentRow()
        if row < 0 or row >= len(self._session.active_filters):
            self._show_error("Bitte einen aktiven Filter auswaehlen.")
            return

        removed = self._session.active_filters[row].to_display_text()
        self._session.remove_filter_at(row)
        self.refresh_view_state()
        self._update_status(f"Filter entfernt: {removed}.")
        self._refresh_main_window()

    def _on_reset_filter(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        self._session.clear_filters()
        self.refresh_view_state()
        self._update_status("Alle Filter zurueckgesetzt.")
        self._refresh_main_window()

    def _on_return_to_full_view(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        self._session.clear_quick_view_mode()
        self.refresh_view_state()
        self._update_status("Zur Gesamtansicht zurueckgekehrt.")
        self._refresh_main_window()

    def _on_sort(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        column = self._col_combo.currentText()
        if not column:
            self._show_error("Keine Spalte ausgewaehlt.")
            return

        sort_state = SortState(column=column, ascending=self._sort_asc_radio.isChecked())
        result = apply_sort(self._session.working_df, sort_state)
        if not result.success or result.df is None:
            self._show_error(result.message)
            return

        self._session.sort_state = sort_state
        self._session.working_df = result.df
        self._update_status(result.message)
        self._refresh_main_window()

    def _on_focus_missing(self) -> None:
        self._set_quick_view("missing", focus_missing_rows)

    def _on_focus_duplicates(self) -> None:
        self._set_quick_view("duplicates", focus_duplicate_rows)

    def _on_focus_outliers(self) -> None:
        self._set_quick_view("outliers", focus_outlier_candidates)

    def _set_quick_view(self, mode: str, func) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        previous_mode = self._session.quick_view_mode
        if previous_mode is not None:
            self._session.clear_quick_view_mode()

        result = func(self._session.current_df)
        if not result.success:
            if previous_mode is not None:
                self._session.set_quick_view_mode(previous_mode)
            self._show_error(result.message)
            return

        self._session.set_quick_view_mode(mode)
        self.refresh_view_state()
        self._update_status(result.message)
        self._refresh_main_window()

    def _on_toggle_duplicates(self, checked: bool) -> None:
        if not self._session.has_data:
            self._mark_duplicates_toggle.blockSignals(True)
            self._mark_duplicates_toggle.setChecked(False)
            self._mark_duplicates_toggle.blockSignals(False)
            return

        self._sync_duplicate_marking()
        self._update_mark_toggle_labels()
        self._update_status("Dublettenmarkierung aktiviert." if checked else "Dublettenmarkierung deaktiviert.")
        self._refresh_main_window()

    def _on_toggle_missing(self, checked: bool) -> None:
        if not self._session.has_data:
            self._mark_missing_toggle.blockSignals(True)
            self._mark_missing_toggle.setChecked(False)
            self._mark_missing_toggle.blockSignals(False)
            return

        self._sync_missing_marking()
        self._update_mark_toggle_labels()
        self._update_status("Fehlwertmarkierung aktiviert." if checked else "Fehlwertmarkierung deaktiviert.")
        self._refresh_main_window()

    def _on_apply_type(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        column = self._col_combo.currentText()
        if not column:
            self._show_error("Keine Spalte ausgewaehlt.")
            return

        type_map = {
            1: ColumnType.NUMERIC,
            2: ColumnType.CATEGORICAL,
            3: ColumnType.DATETIME,
            4: ColumnType.ID,
            5: ColumnType.TEXT,
        }

        manual_types = self._session.manual_column_types.copy()
        if self._type_combo.currentIndex() == 0:
            manual_types.pop(column, None)
            self._session.manual_column_types = manual_types
            self._update_status(f"Typ fuer Spalte '{column}' auf automatisch zurueckgesetzt.")
        else:
            column_type = type_map.get(self._type_combo.currentIndex())
            if column_type is None:
                self._show_error("Ungueltiger Spaltentyp.")
                return
            manual_types[column] = column_type
            self._session.manual_column_types = manual_types
            self._update_status(f"Typ fuer Spalte '{column}' auf {column_type.name} gesetzt.")

        self._refresh_main_window()

    def _on_reset_type(self) -> None:
        if not self._session.has_data:
            self._show_error("Keine Daten geladen.")
            return

        self._session.manual_column_types = {}
        self._update_status("Alle Typuebersteuerungen zurueckgesetzt.")
        self._refresh_main_window()

    def _build_filter_condition(self) -> FilterCondition | None:
        column = self._col_combo.currentText()
        if not column:
            self._show_error("Keine Spalte ausgewaehlt.")
            return None

        operator_map = {
            0: FilterOperator.EQUAL,
            1: FilterOperator.NOT_EQUAL,
            2: FilterOperator.GREATER_THAN,
            3: FilterOperator.LESS_THAN,
            4: FilterOperator.BETWEEN,
            5: FilterOperator.CONTAINS,
            6: FilterOperator.STARTS_WITH,
            7: FilterOperator.IS_EMPTY,
            8: FilterOperator.IS_NOT_EMPTY,
        }
        operator = operator_map.get(self._filter_op_combo.currentIndex())
        if operator is None:
            self._show_error("Ungueltiger Operator.")
            return None

        value1 = self._filter_value1_edit.text().strip()
        value2 = self._filter_value2_edit.text().strip()

        if operator in (FilterOperator.IS_EMPTY, FilterOperator.IS_NOT_EMPTY):
            return FilterCondition(column=column, operator=operator)

        if operator == FilterOperator.BETWEEN:
            if not value1 or not value2:
                self._show_error("Fuer Bereichsfilter werden zwei Werte benoetigt.")
                return None
            return FilterCondition(column=column, operator=operator, value=value1, value2=value2)

        if not value1:
            self._show_error("Ein Wert ist erforderlich.")
            return None

        return FilterCondition(column=column, operator=operator, value=value1)

    def _rename_view_state_references(self, old_name: str, new_name: str) -> None:
        renamed_filters = []
        for condition in self._session.active_filters:
            if condition.column == old_name:
                renamed_filters.append(
                    FilterCondition(
                        column=new_name,
                        operator=condition.operator,
                        value=condition.value,
                        value2=condition.value2,
                    )
                )
            else:
                renamed_filters.append(condition)
        self._session.active_filters = renamed_filters

        hidden = [new_name if col == old_name else col for col in self._session.hidden_columns]
        self._session.hidden_columns = hidden

        manual_types = self._session.manual_column_types.copy()
        if old_name in manual_types:
            manual_types[new_name] = manual_types.pop(old_name)
            self._session.manual_column_types = manual_types

    def _remove_view_state_references(self, column: str) -> None:
        self._session.active_filters = [
            condition for condition in self._session.active_filters if condition.column != column
        ]
        self._session.hidden_columns = [col for col in self._session.hidden_columns if col != column]

        manual_types = self._session.manual_column_types.copy()
        if column in manual_types:
            del manual_types[column]
            self._session.manual_column_types = manual_types

    def _refresh_main_window(self) -> None:
        if self._main_window:
            self._main_window._refresh_after_edit()

    def _update_status(self, message: str) -> None:
        self._status_label.setText(message)

    def _show_error(self, message: str) -> None:
        QMessageBox.warning(self, "Fehler", message)

    def _sync_markings(self) -> None:
        self._sync_duplicate_marking()
        self._sync_missing_marking()

    def _sync_duplicate_marking(self) -> None:
        if not self._session.has_data or not self._mark_duplicates_toggle.isChecked():
            self._session.duplicate_marking = None
            return
        self._session.duplicate_marking = mark_duplicates(self._session.current_df)

    def _sync_missing_marking(self) -> None:
        if not self._session.has_data or not self._mark_missing_toggle.isChecked():
            self._session.missing_marking = None
            return
        self._session.missing_marking = mark_missing(self._session.current_df)

    def _update_mark_toggle_labels(self) -> None:
        self._mark_duplicates_toggle.setText(
            "Dubletten: EIN" if self._mark_duplicates_toggle.isChecked() else "Dubletten: AUS"
        )
        self._mark_missing_toggle.setText(
            "Fehlwerte: EIN" if self._mark_missing_toggle.isChecked() else "Fehlwerte: AUS"
        )

    def _apply_responsive_layout(self, force: bool = False) -> None:
        available_width = self._scroll_area.viewport().width() if self._scroll_area else self.width()
        use_two_columns = available_width >= self._TWO_COLUMN_BREAKPOINT

        if not force and self._two_column_mode == use_two_columns:
            return

        self._two_column_mode = use_two_columns
        self._move_groups_to_layout_mode(use_two_columns)

    def _move_groups_to_layout_mode(self, use_two_columns: bool) -> None:
        groups = self._left_groups + self._right_groups
        for widget in groups:
            widget.setParent(None)

        self._clear_layout(self._left_layout)
        self._clear_layout(self._right_layout)
        self._clear_layout(self._single_layout)

        if use_two_columns:
            self._content_row.show()
            self._left_column.show()
            self._right_column.show()
            self._single_column.hide()

            for widget in self._left_groups:
                self._left_layout.addWidget(widget)
            self._left_layout.addStretch()

            for widget in self._right_groups:
                self._right_layout.addWidget(widget)
            self._right_layout.addStretch()
        else:
            self._content_row.hide()
            self._single_column.show()

            for widget in groups:
                self._single_layout.addWidget(widget)
            self._single_layout.addStretch()

    @staticmethod
    def _clear_layout(layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.setParent(None)
            elif child_layout is not None:
                EditPanel._clear_layout(child_layout)
