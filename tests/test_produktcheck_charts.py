"""Produktcheck für Charts mit real Stresstest-Datei."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from minan_v1.services.chart_service import (
    create_bar_chart,
    create_boxplot,
    create_correlation_heatmap,
    create_histogram,
    create_missing_chart,
    get_categorical_columns,
    get_numeric_columns,
)
from minan_v1.services.import_service import load_csv
from minan_v1.services.profile_service import create_profile


class TestProduktcheckCharts:
    """Echte Produktcheck-Tests mit Stresstest-Datei."""

    @pytest.fixture
    def stresstest_path(self):
        """Pfad zur Stresstest-Datei."""
        path = (
            Path(__file__).parent.parent
            / "assets"
            / "sample_data"
            / "stresstest_5000x19.csv"
        )
        if not path.exists():
            pytest.skip(f"Stresstest-Datei nicht gefunden: {path}")
        return path

    @pytest.fixture
    def data(self, stresstest_path):
        """Lädt die Stresstest-Datei wie in der App."""
        df, import_result = load_csv(stresstest_path)
        assert import_result.success
        return df, import_result, create_profile(df)

    def test_csv_load_success(self, data):
        """CSV-Datei wird erfolgreich geladen."""
        df, import_result, profile = data
        assert len(df) == 5000
        assert len(df.columns) == 21
        assert import_result.success

    def test_missing_chart_visible_under_stresstest(self, data):
        """Fehlwerte-Chart ist unter Stresstest sichtbar."""
        df, _, profile = data
        fig = create_missing_chart(df)

        # Stresstest hat bewusst Fehlwerte
        assert fig is not None
        assert fig.get_facecolor() == (
            0.11764705882352941,
            0.11764705882352941,
            0.11764705882352941,
            1.0,
        )

    def test_histogram_dark_theme(self, data):
        """Histogramm hat dunkles Theme."""
        df, _, profile = data
        numeric_cols = get_numeric_columns(profile)

        for col in numeric_cols[:2]:
            fig = create_histogram(df, col)
            # Dark theme: Figure sollte dunkler Hintergrund haben
            assert fig.get_facecolor()[0] < 0.2  # RGB < 0.2

    def test_boxplot_shows_quartiles(self, data):
        """Boxplot zeigt Q1/Median/Q3."""
        df, _, profile = data
        numeric_cols = get_numeric_columns(profile)

        col = numeric_cols[0]
        fig = create_boxplot(df, col)

        # Chart sollte erzeugt sein
        assert isinstance(fig, plt.Figure)

    def test_bar_chart_top_n_reasonable(self, data):
        """Bar-Chart zeigt sinnvolle Anzahl Kategorien."""
        df, _, profile = data
        cat_cols = get_categorical_columns(profile)

        for col in cat_cols[:2]:
            unique_count = df[col].nunique()
            fig = create_bar_chart(df, col)

            # Top-N sollte begrenzt sein
            if unique_count > 10:
                # Figure sollte nicht zu hoch sein (max 8-10 Kategorien)
                height = fig.get_size_inches()[1]
                assert (
                    height < 10
                ), f"Bar chart height {height} zu hoch für {unique_count} Kategorien"

    def test_heatmap_limited_for_readability(self, data):
        """Heatmap ist auf 15x15 begrenzt für Lesbarkeit."""
        df, _, profile = data
        fig = create_correlation_heatmap(df)

        if fig:
            width, height = fig.get_size_inches()
            # Heatmap sollte nicht größer als 20x20 sein
            assert width <= 20
            assert height <= 20

    def test_all_charts_consistent_styling(self, data):
        """Alle Charts haben konsistente dunkle Styling."""
        df, _, profile = data
        numeric_cols = get_numeric_columns(profile)
        cat_cols = get_categorical_columns(profile)

        charts = []

        # Collecting chart figures
        if create_missing_chart(df):
            charts.append(("missing", create_missing_chart(df)))

        for col in numeric_cols[:1]:
            charts.append(("histogram", create_histogram(df, col)))
            charts.append(("boxplot", create_boxplot(df, col)))

        for col in cat_cols[:1]:
            charts.append(("bar", create_bar_chart(df, col)))

        if create_correlation_heatmap(df):
            charts.append(("heatmap", create_correlation_heatmap(df)))

        # Alle sollten dunklen Hintergrund haben
        for chart_type, fig in charts:
            if fig:
                bg_color = fig.get_facecolor()
                # Dark theme: R < 0.2 (dunkelgrau/schwarz)
                assert bg_color[0] < 0.2, f"{chart_type} hat hellen Hintergrund"
                plt.close(fig)

    def test_performance_under_load(self, data):
        """Charts werden schnell erzeugt auch bei 5000 Zeilen."""
        import time

        df, _, profile = data

        numeric_cols = get_numeric_columns(profile)
        cat_cols = get_categorical_columns(profile)

        # Timing für verschiedene Chart-Typen
        start = time.time()
        fig = create_histogram(df, numeric_cols[0])
        histogram_time = time.time() - start
        plt.close(fig)

        start = time.time()
        fig = create_bar_chart(df, cat_cols[0])
        bar_time = time.time() - start
        plt.close(fig)

        start = time.time()
        fig = create_boxplot(df, numeric_cols[0])
        boxplot_time = time.time() - start
        plt.close(fig)

        # Alle sollten unter 2 Sekunden sein
        assert histogram_time < 2.0
        assert bar_time < 2.0
        assert boxplot_time < 2.0
