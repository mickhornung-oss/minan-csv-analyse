"""Tests fuer den HTML-Report-Service."""

from pathlib import Path

from minan_v1.domain.models import FilterCondition, FilterOperator
from minan_v1.domain.session_state import SessionState
from minan_v1.resources import default_report_path
from minan_v1.services.import_service import load_csv
from minan_v1.services.profile_service import create_profile
from minan_v1.services.quality_service import compute_quality_report
from minan_v1.services.report_service import build_report_filename, export_html_report
from minan_v1.services.summary_service import generate_summary


def _prepare_session(csv_path: Path) -> SessionState:
    df, import_result = load_csv(csv_path)
    assert import_result.success
    session = SessionState()
    session.load(df, csv_path)
    session.import_result = import_result
    session.profile = create_profile(session.current_df, session.manual_column_types)
    session.quality_report = compute_quality_report(session.current_df, session.profile)
    session.summary = generate_summary(session.profile, session.quality_report)
    return session


class TestReportService:
    def test_report_filename_format(self):
        name = build_report_filename()
        assert name.startswith("MinAn_Bericht_")
        assert name.endswith(".html")

    def test_default_report_path_points_to_output_reports(self):
        path = default_report_path(build_report_filename())
        assert "output" in path.parts
        assert "reports" in path.parts

    def test_html_report_created(self, tmp_path, sample_df):
        csv_path = tmp_path / "input.csv"
        sample_df.to_csv(csv_path, index=False)
        session = _prepare_session(csv_path)

        target = tmp_path / "bericht"
        result = export_html_report(session, target)

        assert result.success is True
        assert result.file_path.exists()
        html_text = result.file_path.read_text(encoding="utf-8")
        assert "MinAn 1.4 - Analysebericht" in html_text
        assert "Aktive Sicht" in html_text
        assert "data:image/png;base64" in html_text

    def test_report_uses_filtered_active_view(self, tmp_path, sample_df):
        csv_path = tmp_path / "input.csv"
        sample_df.to_csv(csv_path, index=False)
        session = _prepare_session(csv_path)
        session.add_filter(FilterCondition("Stadt", FilterOperator.EQUAL, "Berlin"))
        session.set_quick_view_mode("outliers")
        session.profile = create_profile(
            session.current_df, session.manual_column_types
        )
        session.quality_report = compute_quality_report(
            session.current_df, session.profile
        )
        session.summary = generate_summary(session.profile, session.quality_report)

        target = tmp_path / "filtered_report.html"
        result = export_html_report(session, target)

        assert result.success is True
        html_text = target.read_text(encoding="utf-8")
        assert "1 Filter aktiv" in html_text
        assert "Schnellansicht: Ausreisser-Kandidaten" in html_text
        assert f"Zeilen in der aktuell sichtbaren Analyseansicht</p>" in html_text
        assert f'<div class="stat">{len(session.current_df)}</div>' in html_text
        assert "Stadt = Berlin" in html_text

    def test_report_contains_summary_and_findings(self, tmp_path, df_with_problems):
        csv_path = tmp_path / "problems.csv"
        df_with_problems.to_csv(csv_path, index=False)
        session = _prepare_session(csv_path)

        target = tmp_path / "problem_report.html"
        result = export_html_report(session, target)

        assert result.success is True
        html_text = target.read_text(encoding="utf-8")
        assert "Zusammenfassung" in html_text
        assert "Zentrale Datenqualitaetsbefunde" in html_text
        # Quality findings sind in jedem Fall vorhanden (können verschiedene Formen haben)
        assert "Spalte" in html_text or "Zeile" in html_text or "Duplikat" in html_text

    def test_report_does_not_modify_original_file_or_original_df(
        self, tmp_path, sample_df
    ):
        csv_path = tmp_path / "original.csv"
        sample_df.to_csv(csv_path, index=False)
        original_bytes = csv_path.read_bytes()
        session = _prepare_session(csv_path)
        original_df = session.original_df.copy(deep=True)

        result = export_html_report(session, tmp_path / "unchanged.html")

        assert result.success is True
        assert csv_path.read_bytes() == original_bytes
        assert session.original_df.equals(original_df)

    def test_report_creates_missing_parent_dir(self, tmp_path, sample_df):
        csv_path = tmp_path / "input.csv"
        sample_df.to_csv(csv_path, index=False)
        session = _prepare_session(csv_path)

        target = tmp_path / "reports" / "nested" / "bericht.html"
        result = export_html_report(session, target)

        assert result.success is True
        assert target.exists()
