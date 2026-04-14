"""Tests fuer portable Pfad- und Output-Logik."""

from minan_v1.config import SAMPLE_FILE_NAME
from minan_v1.resources import (
    default_csv_export_dir,
    default_csv_export_path,
    default_report_dir,
    default_report_path,
    ensure_runtime_dirs,
    is_internal_path,
    release_sample_data_dir,
    runtime_root,
    sample_data_path,
    shortstart_readme_path,
)


class TestRuntimePaths:
    def test_runtime_dirs_created(self):
        ensure_runtime_dirs()
        assert default_report_dir().exists()
        assert default_csv_export_dir().exists()

    def test_default_report_path_is_under_output_reports(self):
        path = default_report_path("test.html")
        assert path.parent == default_report_dir()
        assert "output" in path.parts
        assert "reports" in path.parts
        assert not is_internal_path(path)

    def test_default_csv_path_is_under_output_csv(self):
        path = default_csv_export_path("test.csv")
        assert path.parent == default_csv_export_dir()
        assert "output" in path.parts
        assert "csv" in path.parts
        assert not is_internal_path(path)

    def test_sample_file_resolves_from_sample_data(self):
        path = sample_data_path(SAMPLE_FILE_NAME)
        assert path.exists()
        assert path.name == SAMPLE_FILE_NAME
        assert "sample_data" in path.parts
        assert not is_internal_path(path)

    def test_release_sample_dir_is_prepared_under_internal(self):
        path = release_sample_data_dir()
        assert path.name == "sample_data"
        assert "_internal" in path.parts
        assert path.parent.name == "_internal"

    def test_shortstart_readme_path_not_in_internal(self):
        path = shortstart_readme_path()
        assert path.name == "README_Kurzstart.txt"
        assert runtime_root() == path.parent
        assert not is_internal_path(path)
