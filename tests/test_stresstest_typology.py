"""Tests fuer Typklassifikation und Kennzahlen-Konsistenz unter dem Stresstest."""

from pathlib import Path

import pandas as pd
import pytest

from minan_v1.domain.enums import ColumnType
from minan_v1.services.profile_service import create_profile


class TestStressTestTypology:
    """Typklassifikation unter dem 5000-Zeilen-Stresstest pruefen."""

    @pytest.fixture
    def stresstest_df(self):
        """Laden der Stresstest-Datei."""
        path = (
            Path(__file__).parent.parent
            / "assets"
            / "sample_data"
            / "stresstest_5000x19.csv"
        )
        if not path.exists():
            pytest.skip(f"Stresstest-Datei nicht gefunden: {path}")
        return pd.read_csv(path)

    def test_stresstest_loads(self, stresstest_df):
        """Stresstest-Datei ladet erfolgreich."""
        assert len(stresstest_df) == 5000
        assert len(stresstest_df.columns) == 21

    def test_column_type_classification(self, stresstest_df):
        """Typklassifikation ist konsistent."""
        profile = create_profile(stresstest_df)

        # Fasse Spaltentypen zusammen
        type_counts = {}
        for col in profile.columns:
            col_type = col.column_type
            type_counts[col_type] = type_counts.get(col_type, 0) + 1

        # Summe muss gleich Spaltenanzahl sein
        total_types = sum(type_counts.values())
        assert total_types == profile.column_count
        assert total_types == 21

    def test_id_columns_correctly_classified(self, stresstest_df):
        """ID-Spalten werden korrekt erkannt."""
        profile = create_profile(stresstest_df)

        id_columns = [c for c in profile.columns if c.column_type == ColumnType.ID]
        id_names = {c.name for c in id_columns}

        # Wir erwarten: KundenNummer, Bestellnummer (Text-ID)
        assert "KundenNummer" in id_names
        # Email sollte NICHT als ID klassifiziert werden (zu viel Eindeutigkeit aber ohne ID-Keywords)
        email_cols = [c for c in profile.columns if c.name == "Email"]
        assert email_cols[0].column_type != ColumnType.ID

    def test_numeric_columns(self, stresstest_df):
        """Numerische Spalten werden korrekt erkannt."""
        profile = create_profile(stresstest_df)

        numeric_cols = [
            c for c in profile.columns if c.column_type == ColumnType.NUMERIC
        ]
        numeric_names = {c.name for c in numeric_cols}

        # Erwartet: Umsatz, Menge, Rabatt_Prozent, Alter, Gewicht_kg, etc.
        assert "Umsatz" in numeric_names
        assert "Menge" in numeric_names
        assert "Rabatt_Prozent" in numeric_names
        assert "Alter" in numeric_names
        assert "Gewicht_kg" in numeric_names

        # Numeric-Spalten sollten Kennzahlen haben
        for col in numeric_cols:
            if col.count > 0:  # Wenn Datenwerte vorhanden
                assert col.mean is not None, f"{col.name} hat mean=None"
                assert col.median is not None, f"{col.name} hat median=None"
                assert col.min_val is not None, f"{col.name} hat min_val=None"
                assert col.max_val is not None, f"{col.name} hat max_val=None"

    def test_categorical_columns(self, stresstest_df):
        """Kategorische Spalten werden korrekt erkannt."""
        profile = create_profile(stresstest_df)

        cat_cols = [
            c for c in profile.columns if c.column_type == ColumnType.CATEGORICAL
        ]
        cat_names = {c.name for c in cat_cols}

        # Erwartet: Kundentyp, Region, Produktkategorie, Status, Zahlungsart, etc.
        assert "Kundentyp" in cat_names
        assert "Region" in cat_names
        assert "Produktkategorie" in cat_names
        assert "Status" in cat_names

    def test_datetime_columns(self, stresstest_df):
        """Datums-Spalten werden korrekt erkannt."""
        profile = create_profile(stresstest_df)

        dt_cols = [c for c in profile.columns if c.column_type == ColumnType.DATETIME]
        dt_names = {c.name for c in dt_cols}

        # Bestelldatum und Lieferdatum sollten DATETIME sein
        assert "Bestelldatum" in dt_names
        assert "Lieferdatum" in dt_names

    def test_constant_columns_detected(self, stresstest_df):
        """Konstante Spalten werden erkannt."""
        profile = create_profile(stresstest_df)

        constant_cols = [c for c in profile.columns if c.is_constant]
        constant_names = {c.name for c in constant_cols}

        # Firma und Währung sollten konstant sein
        assert "Firma" in constant_names
        assert "Währung" in constant_names

    def test_missing_values_logic(self, stresstest_df):
        """Fehlende Werte werden korrekt gezaelt."""
        profile = create_profile(stresstest_df)

        # Kundennote und Zweites_Produkt haben bewusst Fehlwerte
        kundennote_col = next(c for c in profile.columns if c.name == "Kundennote")
        zweites_produkt_col = next(
            c for c in profile.columns if c.name == "Zweites_Produkt"
        )

        assert kundennote_col.missing > 0
        assert kundennote_col.missing_pct > 0
        assert zweites_produkt_col.missing > 0

    def test_type_sums_are_consistent(self, stresstest_df):
        """Typ-Summen sind in sich konsistent."""
        profile = create_profile(stresstest_df)

        # Summe aller Typ-Zaeler muss Spaltenanzahl sein
        total = (
            profile.numeric_columns
            + profile.categorical_columns
            + profile.datetime_columns
            + profile.id_columns
            + profile.text_columns
            + profile.unknown_columns
        )

        # Hinweis: boolean_columns ist Unterkategorie von categorical
        # Daher muss die Summe auf alle Spalten aufgehen
        assert total == profile.column_count

    def test_unique_value_detection(self, stresstest_df):
        """Eindeutige Werte werden korrekt gezaelt."""
        profile = create_profile(stresstest_df)

        # KundenNummer sollte 5000 eindeutige Werte haben
        kunden_col = next(c for c in profile.columns if c.name == "KundenNummer")
        assert kunden_col.unique == 5000

        # Region sollte 5 eindeutige Werte haben
        region_col = next(c for c in profile.columns if c.name == "Region")
        assert region_col.unique == 5


class TestMetricsConsistency:
    """Kennzahlen-Konsistenz pruefen."""

    @pytest.fixture
    def stresstest_df(self):
        """Laden der Stresstest-Datei."""
        path = (
            Path(__file__).parent.parent
            / "assets"
            / "sample_data"
            / "stresstest_5000x19.csv"
        )
        if not path.exists():
            pytest.skip(f"Stresstest-Datei nicht gefunden: {path}")
        return pd.read_csv(path)

    def test_numeric_metrics_complete(self, stresstest_df):
        """Numerische Spalten haben vollständige Kennzahlen."""
        profile = create_profile(stresstest_df)

        for col in profile.columns:
            if col.column_type == ColumnType.NUMERIC and col.count > 0:
                # Q1 und Q3 sollten vorhanden sein
                assert col.q1 is not None
                assert col.q3 is not None

    def test_quantile_logic(self, stresstest_df):
        """Q1 < Median < Q3 ist logisch konsistent."""
        profile = create_profile(stresstest_df)

        for col in profile.columns:
            if col.column_type == ColumnType.NUMERIC and col.count > 0:
                if col.q1 is not None and col.median is not None and col.q3 is not None:
                    assert col.q1 <= col.median, f"{col.name}: Q1 > Median"
                    assert col.median <= col.q3, f"{col.name}: Median > Q3"
