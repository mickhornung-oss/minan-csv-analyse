"""Produktnaher GUI-Smoke fuer den Hauptpfad (offscreen)."""

from minan_v1.domain.session_state import SessionState
from minan_v1.services.export_service import export_csv
from minan_v1.ui.main_window import MainWindow


def test_gui_main_path_smoke(tmp_path, qapp):
    """Prueft einen durchgehenden Hauptpfad: Laden -> Ansicht -> Export."""
    session = SessionState()
    window = MainWindow(session)
    window.show()
    qapp.processEvents()

    assert window.load_sample_dataset() is True
    qapp.processEvents()
    assert session.current_df is not None
    assert len(session.current_df) > 0

    for tab_index in range(window._tabs.count()):
        window._tabs.setCurrentIndex(tab_index)
        qapp.processEvents()

    # Schnellansicht aktivieren und Reanalyse durchlaufen lassen.
    session.set_quick_view_mode("missing")
    window._refresh_after_edit()
    qapp.processEvents()
    assert len(session.current_df) <= len(session.working_df)

    csv_target = tmp_path / "gui_smoke_export.csv"
    csv_result = export_csv(
        session.current_df,
        csv_target,
        hidden_columns=session.hidden_columns,
    )
    assert csv_result.success is True
    assert csv_target.exists()

    report_target = tmp_path / "gui_smoke_report.html"
    report_result = window.export_report_to_path(report_target)
    assert report_result.success is True
    assert report_target.exists()

    window.close()
