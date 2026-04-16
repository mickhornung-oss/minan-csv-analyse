"""Chart-Service: Standarddiagramme für die CSV-Analyse via matplotlib."""

from typing import Optional

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from minan_v1.config import HISTOGRAM_BINS, TOP_N_VALUES
from minan_v1.domain.enums import ColumnType
from minan_v1.domain.models import DatasetProfile


# --- Dark Theme Konfiguration ---
def _configure_dark_theme():
    """Konfiguriert matplotlib für dunkles Theme."""
    plt.style.use("default")
    plt.rcParams["figure.facecolor"] = "#1e1e1e"
    plt.rcParams["axes.facecolor"] = "#2d2d2d"
    plt.rcParams["axes.edgecolor"] = "#3a3a3a"
    plt.rcParams["axes.labelcolor"] = "#e0e0e0"
    plt.rcParams["text.color"] = "#e0e0e0"
    plt.rcParams["xtick.color"] = "#e0e0e0"
    plt.rcParams["ytick.color"] = "#e0e0e0"
    plt.rcParams["grid.color"] = "#3a3a3a"
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["grid.linewidth"] = 0.5


# Wird beim Import aufgerufen
_configure_dark_theme()


def create_missing_chart(df: pd.DataFrame) -> Optional[Figure]:
    """Balkendiagramm fehlender Werte je Spalte.

    Gibt None zurück, wenn keine Fehlwerte vorhanden.
    """
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=True)

    if missing.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, max(3, len(missing) * 0.4)))
    bars = ax.barh(missing.index.astype(str), missing.values, color="#ff6b6b")
    ax.set_xlabel("Anzahl fehlender Werte", color="#e0e0e0")
    ax.set_title("Fehlende Werte je Spalte", color="#e0e0e0", pad=15)

    # Werte an die Balken schreiben
    for bar, val in zip(bars, missing.values):
        ax.text(
            bar.get_width() + 0.3,
            bar.get_y() + bar.get_height() / 2,
            str(int(val)),
            va="center",
            fontsize=9,
            color="#e0e0e0",
        )

    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    return fig


def create_histogram(
    df: pd.DataFrame, column: str, bins: int = HISTOGRAM_BINS
) -> Figure:
    """Histogramm für eine numerische Spalte mit Dark Theme."""
    data = df[column].dropna()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(data, bins=bins, color="#4a90e2", edgecolor="#2d2d2d", alpha=0.85)
    ax.set_xlabel(column, color="#e0e0e0")
    ax.set_ylabel("Häufigkeit", color="#e0e0e0")
    ax.set_title(f"Histogramm: {column}", color="#e0e0e0", pad=15)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    return fig


def create_boxplot(df: pd.DataFrame, column: str) -> Figure:
    """Boxplot für eine numerische Spalte mit Dark Theme und Q1/Q3 Labels."""
    data = df[column].dropna()

    fig, ax = plt.subplots(figsize=(6, 5))
    bp = ax.boxplot(
        data,
        orientation="vertical",
        patch_artist=True,
        boxprops=dict(facecolor="#4a90e2", alpha=0.6),
        medianprops=dict(color="#ff6b6b", linewidth=2.5),
        whiskerprops=dict(color="#e0e0e0", linewidth=1.5),
        capprops=dict(color="#e0e0e0", linewidth=1.5),
        flierprops=dict(marker="o", markerfacecolor="#ff6b6b", markersize=5, alpha=0.5),
    )

    # Q1, Median, Q3 Werte berechnen für Labels
    q1 = data.quantile(0.25)
    median = data.median()
    q3 = data.quantile(0.75)

    ax.set_ylabel(column, color="#e0e0e0")
    ax.set_title(f"Boxplot: {column}", color="#e0e0e0", pad=15)
    ax.set_xticklabels([column])
    ax.grid(axis="y", alpha=0.2)

    # Zusatzinfo: Q1, Median, Q3 als Text
    info_text = f"Q1: {q1:.2f} | Med: {median:.2f} | Q3: {q3:.2f}"
    ax.text(
        0.5,
        ax.get_ylim()[0],
        info_text,
        ha="center",
        fontsize=8,
        color="#b0b0b0",
        transform=ax.transData,
        bbox=dict(
            boxstyle="round", facecolor="#2d2d2d", alpha=0.8, edgecolor="#3a3a3a"
        ),
    )

    fig.tight_layout()
    return fig


def create_bar_chart(
    df: pd.DataFrame, column: str, top_n: int = TOP_N_VALUES
) -> Figure:
    """Balkendiagramm der Top-N häufigsten Werte einer kategorialen Spalte.

    Passt top_n automatisch an große Datensätze an.
    """
    counts = df[column].value_counts(dropna=True)

    # Intelligente Top-N Anpassung basierend auf Datenumfang
    unique_count = len(counts)
    effective_top_n = min(top_n, max(3, unique_count))

    # Wenn sehr viele Kategorien (>50), reduziere auf 8
    if unique_count > 50:
        effective_top_n = min(8, effective_top_n)

    counts = counts.head(effective_top_n)

    fig, ax = plt.subplots(figsize=(8, max(3, len(counts) * 0.45)))
    bars = ax.barh(counts.index.astype(str)[::-1], counts.values[::-1], color="#52c41a")
    ax.set_xlabel("Häufigkeit", color="#e0e0e0")
    title = f"Top-{len(counts)} Werte: {column}"
    if unique_count > effective_top_n:
        title += f" (von {unique_count} Kategorien)"
    ax.set_title(title, color="#e0e0e0", pad=15)

    # Werte an die Balken schreiben
    for bar, val in zip(bars, counts.values[::-1]):
        ax.text(
            bar.get_width() + 0.3,
            bar.get_y() + bar.get_height() / 2,
            str(int(val)),
            va="center",
            fontsize=9,
            color="#e0e0e0",
        )

    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    return fig


def create_correlation_heatmap(df: pd.DataFrame) -> Optional[Figure]:
    """Korrelations-Heatmap für numerische Spalten mit verbesserter Lesbarkeit.

    Gibt None zurück, wenn weniger als 2 numerische Spalten vorhanden.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()

    # Limit zu viele Spalten (max 15 für Lesbarkeit)
    if len(corr) > 15:
        # Behalte Spalten mit höchster durchschnittlicher Korrelation
        avg_corr = corr.abs().mean(axis=1).sort_values(ascending=False)
        selected_cols = avg_corr.head(15).index
        corr = corr.loc[selected_cols, selected_cols]

    fig, ax = plt.subplots(figsize=(max(6, len(corr) * 0.9), max(5, len(corr) * 0.8)))
    im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1, aspect="auto")

    # Achsenbeschriftung mit besserer Lesbarkeit
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))

    # Spaltenname-Länge begrenzen für Lesbarkeit
    col_labels = [
        name[:15] + "..." if len(name) > 15 else name for name in corr.columns
    ]

    ax.set_xticklabels(col_labels, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(col_labels, fontsize=9)

    # Werte in Zellen schreiben
    for i in range(len(corr)):
        for j in range(len(corr)):
            val = corr.iloc[i, j]
            color = "#ffffff" if abs(val) > 0.6 else "#000000"
            ax.text(
                j, i, f"{val:.2f}", ha="center", va="center", fontsize=8, color=color
            )

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Korrelation", color="#e0e0e0")
    ax.set_title("Korrelationsmatrix", color="#e0e0e0", pad=15)
    fig.tight_layout()
    return fig


def get_numeric_columns(profile: DatasetProfile) -> list[str]:
    """Gibt die Namen der numerischen Spalten zurück."""
    return [c.name for c in profile.columns if c.column_type == ColumnType.NUMERIC]


def get_categorical_columns(profile: DatasetProfile) -> list[str]:
    """Gibt die Namen der kategorialen Spalten zurück."""
    return [c.name for c in profile.columns if c.column_type == ColumnType.CATEGORICAL]
