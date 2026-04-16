"""Tests für Konsistenz unter Stresstest - Block 3 Validierung."""

from pathlib import Path

import pandas as pd
import pytest

from minan_v1.services.import_service import load_csv
from minan_v1.services.profile_service import create_profile
from minan_v1.services.quality_service import compute_quality_report
from minan_v1.services.summary_service import generate_summary


class TestStressTestConsistency:
    """Prüft Konsistenz zwischen Überblick, Summary und Qualitätsbefunden."""

    @pytest.fixture
    def stresstest_data(self):
        """Lädt die Stresstest-Datei."""
        path = (
            Path(__file__).parent.parent
            / "assets"
            / "sample_data"
            / "stresstest_5000x19.csv"
        )
        if not path.exists():
            pytest.skip(f"Stresstest-Datei nicht gefunden: {path}")

        df, import_result = load_csv(path)
        if not import_result.success:
            pytest.skip(f"Laden fehlgeschlagen: {import_result.errors}")

        profile = create_profile(df)
        quality = compute_quality_report(df, profile)
        summary = generate_summary(profile, quality)

        return {
            "df": df,
            "profile": profile,
            "quality": quality,
            "summary": summary,
            "import_result": import_result,
        }

    def test_stresstest_spaltenanzahl_konsistent(self, stresstest_data):
        """Spaltenanzahl ist überall gleich (sollte 21 sein)."""
        df = stresstest_data["df"]
        profile = stresstest_data["profile"]

        assert df.shape[1] == 21, f"DataFrame hat {df.shape[1]} Spalten, erwartet 21"
        assert (
            profile.column_count == 21
        ), f"Profile hat {profile.column_count} Spalten, erwartet 21"

    def test_stresstest_zeilenanzahl_konsistent(self, stresstest_data):
        """Zeilenanzahl ist überall gleich (sollte 5000 sein)."""
        df = stresstest_data["df"]
        profile = stresstest_data["profile"]

        assert len(df) == 5000, f"DataFrame hat {len(df)} Zeilen, erwartet 5000"
        assert (
            profile.row_count == 5000
        ), f"Profile hat {profile.row_count} Zeilen, erwartet 5000"

    def test_stresstest_spaltentypen_korrekt(self, stresstest_data):
        """Spaltentypen sind korrekt klassifiziert."""
        profile = stresstest_data["profile"]

        # Sollte 5 numerische Spalten haben
        assert (
            profile.numeric_columns == 5
        ), f"Expected 5 numeric, got {profile.numeric_columns}"

        # Sollte mindestens 6 kategorische haben
        assert (
            profile.categorical_columns >= 6
        ), f"Expected 6+ categorical, got {profile.categorical_columns}"

        # Sollte 2 Datetime haben
        assert (
            profile.datetime_columns == 2
        ), f"Expected 2 datetime, got {profile.datetime_columns}"

    def test_stresstest_fehlwerte_in_quality(self, stresstest_data):
        """Quality meldet die bekannten Fehlwerte-Spalten."""
        quality = stresstest_data["quality"]

        # Kundennote und Zweites_Produkt sollten hohe Fehlwertquoten haben
        high_missing_names = [name for name, _ in quality.high_missing_columns]

        # Mindestens eine der bekannten Spalten sollte gemeldet werden
        assert any(
            name in high_missing_names for name in ["Kundennote", "Zweites_Produkt"]
        ), f"Expected Kundennote or Zweites_Produkt in high_missing_columns, got {high_missing_names}"

    def test_stresstest_summary_erwähnt_spaltenanzahl(self, stresstest_data):
        """Summary erwähnt die Spaltenanzahl."""
        summary = stresstest_data["summary"]
        summary_text = summary.text.lower()

        # Sollte "21" oder "Spalten" erwähnen
        assert (
            "21" in summary_text or "spalten" in summary_text
        ), f"Summary sollte Spaltenanzahl erwähnen: {summary_text}"

    def test_stresstest_summary_erwähnt_zeilenanzahl(self, stresstest_data):
        """Summary erwähnt die Zeilenanzahl."""
        summary = stresstest_data["summary"]
        summary_text = summary.text.lower()

        # Sollte "5000" oder "zeilen" erwähnen
        assert (
            "5000" in summary_text or "zeilen" in summary_text
        ), f"Summary sollte Zeilenanzahl erwähnen: {summary_text}"

    def test_stresstest_summary_kompakt(self, stresstest_data):
        """Summary ist kompakt (max ~6 Sätze für Lesbarkeit unter Stresstest)."""
        summary = stresstest_data["summary"]

        # Neue Summary sollte nicht zu lang sein
        line_count = len(summary.lines)
        assert line_count <= 7, f"Summary zu lang: {line_count} Sätze, sollte <= 7 sein"

    def test_stresstest_quality_findings_priorisiert(self, stresstest_data):
        """Quality-Findings sind priorisiert (kritische zuerst)."""
        quality = stresstest_data["quality"]

        if len(quality.findings) > 0:
            # Erste Findings sollten kritische sein, dann Warnungen, dann Info
            first_severities = [f.severity for f in quality.findings[:5]]

            # Prüfe dass kritische zuerst kommen (falls vorhanden)
            critical_indices = [
                i for i, s in enumerate(first_severities) if s == "critical"
            ]
            warning_indices = [
                i for i, s in enumerate(first_severities) if s == "warning"
            ]
            info_indices = [i for i, s in enumerate(first_severities) if s == "info"]

            # Wenn kritische und info vorhanden, sollte kritisch zuerst kommen
            if critical_indices and info_indices:
                assert max(critical_indices) < min(
                    info_indices
                ), "Kritische Findings sollten vor Info-Findings kommen"

    def test_stresstest_duplikate_keine(self, stresstest_data):
        """Stresstest sollte keine Duplikate haben."""
        profile = stresstest_data["profile"]
        quality = stresstest_data["quality"]

        # Bekannt: Stresstest hat keine Duplikate
        assert (
            profile.duplicate_rows == 0
        ), f"Expected 0 duplicates, got {profile.duplicate_rows}"
        assert (
            quality.duplicate_rows == 0
        ), f"Expected 0 duplicate_rows, got {quality.duplicate_rows}"

    def test_stresstest_id_spalten_erkannt(self, stresstest_data):
        """ID-ähnliche Spalten werden korrekt erkannt."""
        profile = stresstest_data["profile"]

        # Sollte mindestens 2 ID-ähnliche Spalten haben (KundenNummer, Bestellnummer)
        id_cols = [c for c in profile.columns if c.is_id_like]
        assert len(id_cols) >= 2, f"Expected 2+ ID-like columns, got {len(id_cols)}"

        # Diese sollten KundenNummer und Bestellnummer sein
        id_names = [c.name for c in id_cols]
        assert (
            "KundenNummer" in id_names or "Bestellnummer" in id_names
        ), f"Expected KundenNummer or Bestellnummer in ID cols, got {id_names}"

    def test_stresstest_summary_keine_duplikate_erwähnung(self, stresstest_data):
        """Summary erwähnt Duplikate nicht, wenn keine vorhanden."""
        summary = stresstest_data["summary"]
        quality = stresstest_data["quality"]

        summary_text = summary.text.lower()

        # Wenn keine Duplikate, sollte Summary nicht von Duplikaten sprechen
        if quality.duplicate_rows == 0:
            # Sollte entweder nicht "duplikat" erwähnen oder "keine" + "duplikat"
            if "duplikat" in summary_text:
                assert (
                    "keine" in summary_text
                ), "Sollte 'keine' sagen wenn keine Duplikate"
