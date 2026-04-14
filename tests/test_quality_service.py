"""Tests fuer den Qualitaets-Service."""

import pandas as pd

from minan_v1.services.quality_service import compute_quality_report


class TestQualityService:
    """Testklasse fuer Datenqualitaetspruefung."""

    def test_duplicates_detected(self, df_with_duplicates):
        report = compute_quality_report(df_with_duplicates)
        assert report.duplicate_rows == 2

    def test_empty_columns_detected(self, df_with_problems):
        report = compute_quality_report(df_with_problems)
        assert "Leer" in report.empty_columns

    def test_constant_columns_detected(self, df_with_problems):
        report = compute_quality_report(df_with_problems)
        assert "Konstant" in report.constant_columns

    def test_high_missing_detected(self, df_with_problems):
        report = compute_quality_report(df_with_problems)
        high_missing_names = [name for name, _ in report.high_missing_columns]
        assert "VieleFehler" in high_missing_names

    def test_findings_not_empty(self, df_with_problems):
        report = compute_quality_report(df_with_problems)
        assert len(report.findings) > 0

    def test_clean_dataframe_no_critical_findings(self):
        df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": ["x", "y", "z", "w", "v"]})
        report = compute_quality_report(df)
        critical = [f for f in report.findings if f.severity == "critical"]
        assert len(critical) == 0

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        report = compute_quality_report(df)
        assert any("keine Zeilen" in f.message for f in report.findings)

    def test_high_cardinality_detected(self):
        df = pd.DataFrame({"UniqueID": list(range(100)), "Gruppe": ["A", "B"] * 50})
        report = compute_quality_report(df)
        high_card_names = [name for name, _ in report.high_cardinality_columns]
        assert "UniqueID" in high_card_names

    def test_findings_are_sorted_by_severity(self):
        df = pd.DataFrame(
            {
                "leer": [None, None, None, None, None],
                "werte": [1, None, None, None, 1],
                "dup": [1, 1, 2, 2, 3],
            }
        )
        report = compute_quality_report(df)
        severities = [f.severity for f in report.findings]
        order = {"critical": 0, "warning": 1, "info": 2}
        assert severities == sorted(severities, key=lambda s: order[s])
