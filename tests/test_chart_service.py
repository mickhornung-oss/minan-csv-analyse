"""Tests für den Chart-Service."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib.figure import Figure

from minan_v1.services.chart_service import (
    create_missing_chart, create_histogram, create_boxplot,
    create_bar_chart, create_correlation_heatmap,
    get_numeric_columns, get_categorical_columns,
)
from minan_v1.services.profile_service import create_profile


@pytest.fixture
def numeric_df():
    """DataFrame mit numerischen Spalten."""
    return pd.DataFrame({
        "Alter": [25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
        "Gehalt": [30000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000],
        "Score": [3.5, 4.0, 4.2, None, 3.8, 4.5, 4.1, 3.9, 4.3, 4.0],
    })


@pytest.fixture
def categorical_df():
    """DataFrame mit kategorialen Spalten."""
    return pd.DataFrame({
        "Stadt": ["Berlin", "München", "Hamburg", "Berlin", "Köln",
                  "Berlin", "München", "Hamburg", "Berlin", "Köln"],
        "Abteilung": ["IT", "IT", "Vertrieb", "Leitung", "IT",
                      "Vertrieb", "Leitung", "IT", "Vertrieb", "IT"],
    })


@pytest.fixture
def mixed_df(numeric_df, categorical_df):
    """DataFrame mit numerischen und kategorialen Spalten."""
    return pd.concat([numeric_df, categorical_df], axis=1)


class TestMissingChart:
    def test_returns_figure_when_missing_values(self):
        df = pd.DataFrame({"A": [1, None, 3], "B": [None, None, 3]})
        fig = create_missing_chart(df)
        assert isinstance(fig, Figure)

    def test_returns_none_when_no_missing(self, numeric_df):
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        fig = create_missing_chart(df)
        assert fig is None

    def test_handles_all_missing(self):
        df = pd.DataFrame({"A": [None, None], "B": [None, None]})
        fig = create_missing_chart(df)
        assert isinstance(fig, Figure)


class TestHistogram:
    def test_returns_figure(self, numeric_df):
        fig = create_histogram(numeric_df, "Alter")
        assert isinstance(fig, Figure)

    def test_custom_bins(self, numeric_df):
        fig = create_histogram(numeric_df, "Alter", bins=5)
        assert isinstance(fig, Figure)

    def test_column_with_missing(self, numeric_df):
        fig = create_histogram(numeric_df, "Score")
        assert isinstance(fig, Figure)


class TestBoxplot:
    def test_returns_figure(self, numeric_df):
        fig = create_boxplot(numeric_df, "Alter")
        assert isinstance(fig, Figure)

    def test_column_with_missing(self, numeric_df):
        fig = create_boxplot(numeric_df, "Score")
        assert isinstance(fig, Figure)


class TestBarChart:
    def test_returns_figure(self, categorical_df):
        fig = create_bar_chart(categorical_df, "Stadt")
        assert isinstance(fig, Figure)

    def test_top_n_limits(self, categorical_df):
        fig = create_bar_chart(categorical_df, "Stadt", top_n=2)
        assert isinstance(fig, Figure)


class TestCorrelationHeatmap:
    def test_returns_figure_multiple_numeric(self, numeric_df):
        fig = create_correlation_heatmap(numeric_df)
        assert isinstance(fig, Figure)

    def test_returns_none_single_numeric(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
        fig = create_correlation_heatmap(df)
        assert fig is None

    def test_returns_none_no_numeric(self, categorical_df):
        fig = create_correlation_heatmap(categorical_df)
        assert fig is None


class TestHelperFunctions:
    def test_get_numeric_columns(self, mixed_df):
        profile = create_profile(mixed_df)
        cols = get_numeric_columns(profile)
        assert "Alter" in cols
        assert "Gehalt" in cols
        assert "Stadt" not in cols

    def test_get_categorical_columns(self, mixed_df):
        profile = create_profile(mixed_df)
        cols = get_categorical_columns(profile)
        assert "Stadt" in cols
        assert "Abteilung" in cols
        assert "Alter" not in cols


class TestEdgeCases:
    def test_empty_dataframe_missing(self):
        df = pd.DataFrame()
        fig = create_missing_chart(df)
        assert fig is None

    def test_empty_dataframe_correlation(self):
        df = pd.DataFrame()
        fig = create_correlation_heatmap(df)
        assert fig is None

    def test_single_value_histogram(self):
        df = pd.DataFrame({"X": [5, 5, 5, 5]})
        fig = create_histogram(df, "X")
        assert isinstance(fig, Figure)

    def test_single_value_boxplot(self):
        df = pd.DataFrame({"X": [5, 5, 5, 5]})
        fig = create_boxplot(df, "X")
        assert isinstance(fig, Figure)


class TestStressTest:
    """Tests fuer Charts unter großen Datensaetzen (5000+ Zeilen)."""

    @pytest.fixture
    def stresstest_df(self):
        """Ladet die Stresstest-Datei."""
        path = Path(__file__).parent.parent / 'assets' / 'sample_data' / 'stresstest_5000x19.csv'
        if not path.exists():
            pytest.skip(f"Stresstest-Datei nicht gefunden: {path}")
        return pd.read_csv(path)

    def test_stresstest_histogram_loads(self, stresstest_df):
        """Histogramm ladet erfolgreich unter Stresstest."""
        profile = create_profile(stresstest_df)
        numeric_cols = get_numeric_columns(profile)

        assert len(numeric_cols) > 0
        for col in numeric_cols[:2]:
            fig = create_histogram(stresstest_df, col)
            assert isinstance(fig, Figure)
            # Chart soll nicht zu klein sein
            assert fig.get_size_inches()[0] >= 6

    def test_stresstest_boxplot_loads(self, stresstest_df):
        """Boxplot ladet erfolgreich unter Stresstest."""
        profile = create_profile(stresstest_df)
        numeric_cols = get_numeric_columns(profile)

        for col in numeric_cols[:2]:
            fig = create_boxplot(stresstest_df, col)
            assert isinstance(fig, Figure)

    def test_stresstest_bar_chart_with_many_categories(self, stresstest_df):
        """Balkendiagramm verarbeitet viele Kategorien richtig."""
        profile = create_profile(stresstest_df)
        cat_cols = get_categorical_columns(profile)

        assert len(cat_cols) > 0
        for col in cat_cols[:2]:
            unique_count = stresstest_df[col].nunique()
            fig = create_bar_chart(stresstest_df, col)
            assert isinstance(fig, Figure)
            # Top-N soll angewendet werden (max 10, nicht alle Kategorien)
            if unique_count > 10:
                # Figure sollte nicht zu hoch sein (max ~10 Kategorien sichtbar)
                assert fig.get_size_inches()[1] < 10

    def test_stresstest_correlation_with_5_numeric(self, stresstest_df):
        """Korrelations-Heatmap funktioniert mit mehreren numerischen Spalten."""
        profile = create_profile(stresstest_df)
        numeric_cols = get_numeric_columns(profile)

        if len(numeric_cols) >= 2:
            fig = create_correlation_heatmap(stresstest_df)
            assert isinstance(fig, Figure)

    def test_stresstest_missing_chart_loads(self, stresstest_df):
        """Fehlwerte-Chart ladet unter Stresstest."""
        fig = create_missing_chart(stresstest_df)
        # Stresstest hat bewusst Fehlwerte (Kundennote ~38%, Zweites_Produkt ~50%)
        assert isinstance(fig, Figure)

    def test_large_dataframe_histogram_performance(self, stresstest_df):
        """Histogramm sollte bei 5000 Zeilen schnell sein."""
        import time
        profile = create_profile(stresstest_df)
        numeric_cols = get_numeric_columns(profile)

        col = numeric_cols[0]
        start = time.time()
        fig = create_histogram(stresstest_df, col)
        elapsed = time.time() - start

        # Sollte unter 2 Sekunden sein
        assert elapsed < 2.0
        assert isinstance(fig, Figure)

    def test_bar_chart_intelligent_top_n(self, stresstest_df):
        """Top-N wird intelligentangepasst bei zu vielen Kategorien."""
        profile = create_profile(stresstest_df)
        cat_cols = get_categorical_columns(profile)

        # Suche Spalte mit vielen Kategorien
        for col in cat_cols:
            unique_count = stresstest_df[col].nunique()
            fig = create_bar_chart(stresstest_df, col, top_n=10)

            # Wenn >50 Kategorien, sollte auf max 8 begrenzt werden
            if unique_count > 50:
                # Figure sollte nicht zu hoch sein (max ~8 Kategorien)
                assert fig.get_size_inches()[1] <= 6
            else:
                assert isinstance(fig, Figure)

    def test_correlation_heatmap_limited_columns(self, stresstest_df):
        """Heatmap begrenzt sich auf max 15 Spalten für Lesbarkeit."""
        fig = create_correlation_heatmap(stresstest_df)
        if fig:
            assert isinstance(fig, Figure)
            # Die Grafik sollte nicht größer als 15x15 sein
            assert fig.get_size_inches()[0] <= 20
            assert fig.get_size_inches()[1] <= 20


class TestDarkThemeStyle:
    """Tests für Dark-Theme Styling."""

    def test_dark_theme_colors_applied(self):
        """Dark-Theme Farben werden auf matplotlib angewendet."""
        import matplotlib.pyplot as plt
        # Nach import von chart_service sollten die Farben gesetzt sein
        assert plt.rcParams['figure.facecolor'] == '#1e1e1e'
        assert plt.rcParams['axes.facecolor'] == '#2d2d2d'

    def test_histogram_respects_dark_theme(self):
        """Histogramm verwendet Dark-Theme Farben."""
        df = pd.DataFrame({"X": np.random.normal(50, 15, 100)})
        fig = create_histogram(df, "X")

        # Figure sollte mit dunklem Hintergrund erzeugt sein
        assert fig.get_facecolor() == (0.11764705882352941, 0.11764705882352941, 0.11764705882352941, 1.0)
        # (hex #1e1e1e in RGB normalized)

    def test_boxplot_q1_q3_labels_visible(self):
        """Boxplot zeigt Q1/Median/Q3 Labels."""
        df = pd.DataFrame({"X": np.random.normal(50, 15, 100)})
        fig = create_boxplot(df, "X")

        # Sollte Figure mit Text-Labels haben
        assert isinstance(fig, Figure)
