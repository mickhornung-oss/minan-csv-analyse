"""Tests für den Summary-Service."""

import pandas as pd
import pytest

from minan_v1.services.profile_service import create_profile
from minan_v1.services.quality_service import compute_quality_report
from minan_v1.services.summary_service import generate_summary


class TestSummaryService:
    """Testklasse für regelbasierte Kurzzusammenfassung."""

    def _make_summary(self, df: pd.DataFrame):
        profile = create_profile(df)
        quality = compute_quality_report(df)
        return generate_summary(profile, quality)

    def test_summary_not_empty(self, sample_df):
        """Zusammenfassung ist nicht leer."""
        summary = self._make_summary(sample_df)
        assert len(summary.lines) > 0
        assert len(summary.text) > 0

    def test_mentions_row_count(self, sample_df):
        """Zusammenfassung erwähnt die Zeilenanzahl."""
        summary = self._make_summary(sample_df)
        assert "5" in summary.text

    def test_mentions_columns(self, sample_df):
        """Zusammenfassung erwähnt die Spaltenanzahl."""
        summary = self._make_summary(sample_df)
        assert "6" in summary.text or "Spalten" in summary.text

    def test_mentions_missing_when_present(self, sample_df):
        """Zusammenfassung erwähnt fehlende Werte."""
        summary = self._make_summary(sample_df)
        # Neue kompakte Summary: "Fehlwerte insgesamt:" statt mehrfacher Erwähnungen
        assert "fehlwert" in summary.text.lower() or "missing" in summary.text.lower()

    def test_mentions_duplicates_when_present(self, df_with_duplicates):
        """Zusammenfassung erwähnt Duplikate."""
        summary = self._make_summary(df_with_duplicates)
        # Neue kompakte Summary: "Duplikate" statt "doppelte Zeilen"
        assert "duplikat" in summary.text.lower() or "doppelt" in summary.text.lower()

    def test_clean_data_no_warnings(self):
        """Sauberer Datensatz meldet keine Duplikate."""
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
        summary = self._make_summary(df)
        # Neue kompakte Summary: "Keine kritischen Qualitätsprobleme" statt "Keine doppelten"
        assert "keine" in summary.text.lower() and (
            "kritisch" in summary.text.lower() or "doppelt" not in summary.text.lower()
        )

    def test_mentions_empty_columns(self, df_with_problems):
        """Zusammenfassung erwähnt leere Spalten."""
        summary = self._make_summary(df_with_problems)
        assert "leere" in summary.text.lower() or "Leer" in summary.text
