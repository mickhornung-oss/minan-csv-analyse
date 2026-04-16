"""Tests für den CSV-Import-Service."""

from pathlib import Path

import pytest

from minan_v1.services.import_service import load_csv


class TestImportCSV:
    """Testklasse für CSV-Import."""

    def test_load_comma_csv(self, tmp_csv):
        """Komma-CSV wird korrekt geladen."""
        df, result = load_csv(tmp_csv)
        assert result.success
        assert result.row_count == 5
        assert result.column_count == 6
        assert "," in result.separator or result.separator == ","

    def test_load_semicolon_csv(self, tmp_csv_semicolon):
        """Semikolon-CSV wird korrekt geladen."""
        df, result = load_csv(tmp_csv_semicolon)
        assert result.success
        assert result.row_count == 2
        assert result.column_count == 2
        assert result.separator == ";"

    def test_load_latin1_csv(self, tmp_csv_latin1):
        """CSV mit Latin-1 Encoding wird geladen."""
        df, result = load_csv(tmp_csv_latin1)
        assert result.success
        assert result.row_count == 2
        assert "Müller" in df["Name"].values or "M\xfcller" in df["Name"].values

    def test_load_sample_comma(self, sample_data_dir):
        """Beispieldatei mit Komma-Separator laden."""
        path = sample_data_dir / "beispiel_komma.csv"
        if not path.exists():
            pytest.skip("Beispieldatei nicht vorhanden")
        df, result = load_csv(path)
        assert result.success
        assert result.row_count > 0
        assert "Name" in df.columns

    def test_load_sample_semicolon(self, sample_data_dir):
        """Beispieldatei mit Semikolon-Separator laden."""
        path = sample_data_dir / "beispiel_semikolon.csv"
        if not path.exists():
            pytest.skip("Beispieldatei nicht vorhanden")
        df, result = load_csv(path)
        assert result.success
        assert result.separator == ";"

    def test_file_not_found(self, tmp_path):
        """Nicht existierende Datei gibt klaren Fehler."""
        df, result = load_csv(tmp_path / "gibt_es_nicht.csv")
        assert not result.success
        assert "nicht gefunden" in result.error

    def test_empty_file(self, tmp_path):
        """Leere Datei gibt klaren Fehler."""
        empty = tmp_path / "leer.csv"
        empty.write_text("")
        df, result = load_csv(empty)
        assert not result.success
        assert "leer" in result.error.lower()

    def test_original_file_not_modified(self, tmp_csv):
        """Originaldatei wird beim Import nicht verändert."""
        original_content = tmp_csv.read_bytes()
        load_csv(tmp_csv)
        assert tmp_csv.read_bytes() == original_content

    def test_import_result_metadata(self, tmp_csv):
        """ImportResult enthält korrekten Dateinamen und Pfad."""
        df, result = load_csv(tmp_csv)
        assert result.file_name == "test_data.csv"
        assert result.file_path == tmp_csv
        assert result.encoding != ""
