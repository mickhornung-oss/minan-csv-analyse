"""Tests für den Profil-Service."""

import pytest
import pandas as pd

from minan_v1.services.profile_service import create_profile
from minan_v1.domain.enums import ColumnType


class TestProfileService:
    """Testklasse für Datensatz-Profilierung."""

    def test_row_and_column_count(self, sample_df):
        """Zeilen- und Spaltenanzahl stimmen."""
        profile = create_profile(sample_df)
        assert profile.row_count == 5
        assert profile.column_count == 6

    def test_missing_values_detected(self, sample_df):
        """Fehlwerte werden korrekt gezählt."""
        profile = create_profile(sample_df)
        assert profile.total_missing == 2  # Name(1) + Gehalt(1)
        name_col = next(c for c in profile.columns if c.name == "Name")
        assert name_col.missing == 1

    def test_unique_counts(self, sample_df):
        """Unique-Counts stimmen."""
        profile = create_profile(sample_df)
        stadt_col = next(c for c in profile.columns if c.name == "Stadt")
        assert stadt_col.unique == 3  # Berlin, München, Hamburg

    def test_numeric_classification(self, sample_df):
        """Numerische Spalten werden als NUMERIC erkannt."""
        profile = create_profile(sample_df)
        alter_col = next(c for c in profile.columns if c.name == "Alter")
        assert alter_col.column_type == ColumnType.NUMERIC

    def test_categorical_classification(self, sample_df):
        """Kategorische Spalten werden erkannt."""
        profile = create_profile(sample_df)
        stadt_col = next(c for c in profile.columns if c.name == "Stadt")
        assert stadt_col.column_type == ColumnType.CATEGORICAL

    def test_numeric_stats(self, sample_df):
        """Numerische Kennzahlen werden berechnet."""
        profile = create_profile(sample_df)
        alter_col = next(c for c in profile.columns if c.name == "Alter")
        assert alter_col.mean is not None
        assert alter_col.median is not None
        assert alter_col.std is not None
        assert alter_col.min_val is not None
        assert alter_col.max_val is not None
        assert alter_col.q1 is not None
        assert alter_col.q3 is not None
        assert alter_col.min_val == 25
        assert alter_col.max_val == 42

    def test_top_values(self, sample_df):
        """Top-Werte werden erzeugt."""
        profile = create_profile(sample_df)
        stadt_col = next(c for c in profile.columns if c.name == "Stadt")
        assert len(stadt_col.top_values) > 0
        # Berlin kommt 3x vor -> an erster Stelle
        assert stadt_col.top_values[0][0] == "Berlin"

    def test_duplicate_count(self):
        """Duplikate werden im Profil gezählt."""
        df = pd.DataFrame({"A": [1, 2, 1], "B": ["x", "y", "x"]})
        profile = create_profile(df)
        assert profile.duplicate_rows == 1

    def test_id_like_detection(self):
        """ID-ähnliche Spalten werden erkannt."""
        df = pd.DataFrame({"ID": [1, 2, 3, 4, 5], "Val": [10, 10, 10, 10, 10]})
        profile = create_profile(df)
        id_col = next(c for c in profile.columns if c.name == "ID")
        assert id_col.is_id_like

    def test_constant_detection(self):
        """Konstante Spalten werden erkannt."""
        df = pd.DataFrame({"K": ["A", "A", "A"], "V": [1, 2, 3]})
        profile = create_profile(df)
        k_col = next(c for c in profile.columns if c.name == "K")
        assert k_col.is_constant
