#!/usr/bin/env python3
"""Detaillierter Produktcheck fuer Charts mit Stresstest."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent.parent))

from minan_v1.services.chart_service import (  # noqa: E402
    create_bar_chart,
    create_boxplot,
    create_correlation_heatmap,
    create_histogram,
    create_missing_chart,
    get_categorical_columns,
    get_numeric_columns,
)
from minan_v1.services.import_service import load_csv  # noqa: E402
from minan_v1.services.profile_service import create_profile  # noqa: E402

project_root = Path(__file__).resolve().parent.parent
csv_path = project_root / "assets" / "sample_data" / "stresstest_5000x19.csv"

print("=" * 70)
print("MinAn 1.4 BLOCK 2 - DIAGRAMME & CHARTS PRODUKTCHECK")
print("=" * 70)

print("\n[SCHRITT 1] CSV-Datei laden...")
df, import_result = load_csv(csv_path)
if not import_result.success:
    print(f"[ERROR] CSV-Laden fehlgeschlagen: {import_result.error}")
    sys.exit(1)

profile = create_profile(df)
print(f"[OK] Stresstest geladen: {df.shape[0]} Zeilen x {df.shape[1]} Spalten")
print(f"     Encoding: {import_result.encoding}")
print(f"     Separator: {repr(import_result.separator)}")

print("\n[SCHRITT 2] Spaltentypen analysieren...")
numeric_cols = get_numeric_columns(profile)
categorical_cols = get_categorical_columns(profile)
print(f"[OK] Numerisch: {len(numeric_cols)} Spalten - {numeric_cols}")
print(f"[OK] Kategorisch: {len(categorical_cols)} Spalten - {categorical_cols}")

print("\n[SCHRITT 3] Fehlwerte-Diagramm erzeugen...")
try:
    fig = create_missing_chart(df)
    if fig:
        output_file = project_root / "output" / "produktcheck_missing.png"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_file, dpi=100)
        plt.close(fig)
        print(f"[OK] Fehlwerte-Chart erzeugt und gespeichert: {output_file}")
    else:
        print("[SKIP] Keine Fehlwerte in Datensatz")
except (ValueError, TypeError) as exc:
    print(f"[ERROR] Fehlwerte-Chart: {exc}")

print("\n[SCHRITT 4] Histogramme erzeugen...")
for col in numeric_cols[:3]:
    try:
        fig = create_histogram(df, col)
        output_file = project_root / "output" / f"produktcheck_histogram_{col}.png"
        fig.savefig(output_file, dpi=100)
        plt.close(fig)
        print(f"[OK] Histogramm fuer '{col}' erzeugt")
    except (ValueError, TypeError) as exc:
        print(f"[ERROR] Histogramm fuer '{col}': {exc}")

print("\n[SCHRITT 5] Boxplots erzeugen...")
for col in numeric_cols[:2]:
    try:
        fig = create_boxplot(df, col)
        output_file = project_root / "output" / f"produktcheck_boxplot_{col}.png"
        fig.savefig(output_file, dpi=100)
        plt.close(fig)
        print(f"[OK] Boxplot fuer '{col}' erzeugt (mit Q1/Median/Q3 Labels)")
    except (ValueError, TypeError) as exc:
        print(f"[ERROR] Boxplot fuer '{col}': {exc}")

print("\n[SCHRITT 6] Top-Kategorien-Diagramme erzeugen...")
for col in categorical_cols[:3]:
    unique_count = df[col].nunique()
    try:
        fig = create_bar_chart(df, col)
        output_file = project_root / "output" / f"produktcheck_bar_{col}.png"
        fig.savefig(output_file, dpi=100)
        plt.close(fig)
        print(f"[OK] Bar-Chart fuer '{col}' ({unique_count} unique Werte) erzeugt")
    except (ValueError, TypeError) as exc:
        print(f"[ERROR] Bar-Chart fuer '{col}': {exc}")

print("\n[SCHRITT 7] Korrelations-Heatmap erzeugen...")
try:
    fig = create_correlation_heatmap(df)
    if fig:
        output_file = project_root / "output" / "produktcheck_correlation.png"
        fig.savefig(output_file, dpi=100)
        plt.close(fig)
        print("[OK] Korrelations-Heatmap erzeugt")
    else:
        print("[SKIP] Zu wenig numerische Spalten")
except (ValueError, TypeError) as exc:
    print(f"[ERROR] Korrelations-Heatmap: {exc}")

print("\n" + "=" * 70)
print("PRODUKTCHECK ABGESCHLOSSEN")
print("=" * 70)
