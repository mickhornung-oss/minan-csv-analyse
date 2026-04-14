"""Tests fuer den Export-Service."""

import pandas as pd

from minan_v1.services.export_service import export_csv


class TestExportService:
    """Testklasse fuer CSV-Export."""

    def test_export_creates_new_file(self, sample_df, tmp_path):
        export_path = tmp_path / "test_export.csv"
        result = export_csv(sample_df, export_path)

        assert result.success is True
        assert export_path.exists()
        assert export_path.is_file()
        assert result.row_count == len(sample_df)
        assert result.column_count == len(sample_df.columns)

    def test_export_with_hidden_columns(self, sample_df, tmp_path):
        export_path = tmp_path / "test_export_hidden.csv"
        result = export_csv(sample_df, export_path, hidden_columns=["Name"])

        assert result.success is True
        exported_df = pd.read_csv(export_path)
        assert "Name" not in exported_df.columns
        assert result.column_count == len(sample_df.columns) - 1

    def test_export_empty_dataframe(self, tmp_path):
        result = export_csv(pd.DataFrame(), tmp_path / "test_empty.csv")
        assert result.success is False
        assert "keine daten" in result.error.lower()

    def test_export_creates_missing_parent_dir(self, sample_df, tmp_path):
        export_path = tmp_path / "nonexistent" / "test.csv"
        result = export_csv(sample_df, export_path)

        assert result.success is True
        assert export_path.exists()

    def test_export_adds_csv_extension(self, sample_df, tmp_path):
        result = export_csv(sample_df, tmp_path / "test_no_ext")
        assert result.success is True
        assert result.file_path.suffix == ".csv"

    def test_export_all_hidden_columns(self, sample_df, tmp_path):
        export_path = tmp_path / "test_all_hidden.csv"
        result = export_csv(sample_df.copy(), export_path, hidden_columns=sample_df.columns.tolist())

        assert result.success is False
        assert "alle spalten sind ausgeblendet" in result.error.lower()

    def test_export_filtered_view(self, sample_df, tmp_path):
        export_path = tmp_path / "test_filtered.csv"
        filtered_df = sample_df[sample_df["Stadt"] == "Berlin"].copy()

        result = export_csv(filtered_df, export_path)

        assert result.success is True
        exported_df = pd.read_csv(export_path)
        assert len(exported_df) == 3
        assert set(exported_df["Stadt"].tolist()) == {"Berlin"}
        assert len(sample_df) == 5

    def test_export_focus_view_keeps_original_unchanged(self, df_with_outliers, tmp_path):
        export_path = tmp_path / "test_outliers.csv"
        focus_df = df_with_outliers[df_with_outliers["Wert"] == 200].copy()
        original_df = df_with_outliers.copy(deep=True)

        result = export_csv(focus_df, export_path)

        assert result.success is True
        exported_df = pd.read_csv(export_path)
        assert exported_df["Wert"].tolist() == [200]
        assert df_with_outliers.equals(original_df)
