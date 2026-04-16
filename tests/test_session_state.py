"""Tests fuer den Session-State."""

from minan_v1.domain.enums import AnalysisStatus
from minan_v1.domain.models import (
    FilterCondition,
    FilterOperator,
    QualityReport,
    SummaryResult,
)
from minan_v1.domain.session_state import SessionState


class TestSessionState:
    """Testklasse fuer die zentrale Sitzungsverwaltung."""

    def test_initial_state_is_empty(self):
        session = SessionState()
        assert session.status == AnalysisStatus.EMPTY
        assert session.has_data is False

    def test_load_creates_working_copy(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")
        assert session.status == AnalysisStatus.LOADED
        assert session.has_data is True
        assert session.working_df is not session.original_df
        assert session.current_df is not None

    def test_working_copy_is_independent(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")
        session.working_df = session.working_df.drop(columns=["Name"])
        assert "Name" in session.original_df.columns

    def test_reset_clears_session(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")
        session.reset()
        assert session.status == AnalysisStatus.EMPTY
        assert session.has_data is False
        assert session.import_result is None
        assert session.quality_report is None
        assert session.summary is None

    def test_revert_restores_original(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")
        session.working_df = session.working_df.drop(columns=["Name"])
        session.revert_to_original()
        assert session.working_df.shape == sample_df.shape
        assert session.current_df.shape == sample_df.shape

    def test_analysis_results_stored(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")
        session.quality_report = QualityReport(duplicate_rows=2)
        session.summary = SummaryResult(lines=["Testzeile"])
        assert session.quality_report.duplicate_rows == 2
        assert session.summary.text == "Testzeile"

    def test_is_modified_after_change(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")
        assert not session.is_modified
        session.working_df = session.working_df.drop(columns=["Name"])
        assert session.is_modified

    def test_multiple_active_filters_rebuild_current_view(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")

        session.add_filter(FilterCondition("Stadt", FilterOperator.EQUAL, "Berlin"))
        session.add_filter(FilterCondition("Alter", FilterOperator.GREATER_THAN, "30"))

        assert len(session.active_filters) == 2
        assert session.current_df["Name"].tolist() == ["Charlie", "Eve"]
        assert session.working_df.equals(sample_df)

    def test_remove_single_filter_keeps_remaining_filters(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")
        session.add_filter(FilterCondition("Stadt", FilterOperator.EQUAL, "Berlin"))
        session.add_filter(FilterCondition("Alter", FilterOperator.GREATER_THAN, "30"))

        session.remove_filter_at(1)

        assert len(session.active_filters) == 1
        assert session.current_df["Stadt"].tolist() == ["Berlin", "Berlin", "Berlin"]

    def test_reset_all_filters_returns_full_working_view(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")
        session.add_filter(FilterCondition("Stadt", FilterOperator.EQUAL, "Berlin"))
        session.add_filter(FilterCondition("Alter", FilterOperator.GREATER_THAN, "30"))

        session.clear_filters()

        assert session.active_filters == []
        assert session.current_df.equals(session.working_df)

    def test_quick_view_missing_rows(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")

        session.set_quick_view_mode("missing")

        assert session.quick_view_mode == "missing"
        assert session.current_df["ID"].tolist() == [4]

    def test_quick_view_duplicates(self, df_with_duplicates, tmp_path):
        session = SessionState()
        session.load(df_with_duplicates, tmp_path / "test.csv")

        session.set_quick_view_mode("duplicates")

        assert session.quick_view_mode == "duplicates"
        assert len(session.current_df) == 4

    def test_quick_view_outliers(self, df_with_outliers, tmp_path):
        session = SessionState()
        session.load(df_with_outliers, tmp_path / "test.csv")

        session.set_quick_view_mode("outliers")

        assert session.quick_view_mode == "outliers"
        assert session.current_df["Wert"].tolist() == [200]

    def test_clear_quick_view_returns_to_filtered_view(self, sample_df, tmp_path):
        session = SessionState()
        session.load(sample_df, tmp_path / "test.csv")
        session.add_filter(FilterCondition("Stadt", FilterOperator.EQUAL, "Berlin"))
        session.set_quick_view_mode("missing")

        session.clear_quick_view_mode()

        assert session.quick_view_mode is None
        assert session.current_df["Stadt"].tolist() == ["Berlin", "Berlin", "Berlin"]
