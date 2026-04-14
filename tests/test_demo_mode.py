"""Tests fuer Schnellstart- und Beispieldatei-Funktionen."""

from minan_v1.config import SAMPLE_FILE_NAME
from minan_v1.domain.session_state import SessionState
from minan_v1.resources import sample_data_path
from minan_v1.ui.main_window import MainWindow


class TestQuickstartMode:
    def test_sample_path_exists(self):
        path = sample_data_path(SAMPLE_FILE_NAME)
        assert path.exists()
        assert path.name == SAMPLE_FILE_NAME
        assert "sample_data" in path.parts

    def test_sample_dataset_loads_via_main_window(self, qapp):
        session = SessionState()
        window = MainWindow(session)

        ok = window.load_sample_dataset()

        assert ok is True
        assert session.import_result is not None
        assert session.import_result.file_name == SAMPLE_FILE_NAME
        assert session.current_df is not None
        assert len(session.current_df) == 200
        window.close()
