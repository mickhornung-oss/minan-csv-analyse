#!/usr/bin/env python3
"""Produktcheck für Charts unter Stresstest-Datensatz."""

import sys
from pathlib import Path

# Pfade
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from minan_v1.services.profile_service import create_profile
from minan_v1.services.chart_service import (
    create_missing_chart, create_histogram, create_boxplot,
    create_bar_chart, create_correlation_heatmap,
    get_numeric_columns, get_categorical_columns,
)

csv_path = project_root / "assets" / "sample_data" / "stresstest_5000x19.csv"

print("[INFO] Loading stresstest data...")
df = pd.read_csv(csv_path)
profile = create_profile(df)

print(f"[OK] Stresstest loaded: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"[OK] Numeric columns: {get_numeric_columns(profile)}")
print(f"[OK] Categorical columns: {get_categorical_columns(profile)}")

# Test 1: Missing chart
print("\n--- TEST 1: Missing Chart ---")
fig = create_missing_chart(df)
if fig:
    print("[OK] Missing chart created")
    print(f"    Figure size: {fig.get_size_inches()}")
else:
    print("[SKIP] No missing values in dataset")

# Test 2: Histograms
print("\n--- TEST 2: Histograms ---")
numeric_cols = get_numeric_columns(profile)
for col in numeric_cols[:2]:
    try:
        fig = create_histogram(df, col)
        print(f"[OK] Histogram for '{col}' created")
        print(f"    Figure size: {fig.get_size_inches()}")
    except Exception as e:
        print(f"[ERROR] Histogram for '{col}': {e}")

# Test 3: Boxplots
print("\n--- TEST 3: Boxplots ---")
for col in numeric_cols[:2]:
    try:
        fig = create_boxplot(df, col)
        print(f"[OK] Boxplot for '{col}' created")
    except Exception as e:
        print(f"[ERROR] Boxplot for '{col}': {e}")

# Test 4: Bar charts with large categories
print("\n--- TEST 4: Bar Charts ---")
cat_cols = get_categorical_columns(profile)
for col in cat_cols[:3]:
    unique_count = df[col].nunique()
    try:
        fig = create_bar_chart(df, col)
        print(f"[OK] Bar chart for '{col}' ({unique_count} unique) created")
        print(f"    Figure size: {fig.get_size_inches()}")
    except Exception as e:
        print(f"[ERROR] Bar chart for '{col}': {e}")

# Test 5: Correlation heatmap
print("\n--- TEST 5: Correlation Heatmap ---")
try:
    fig = create_correlation_heatmap(df)
    if fig:
        print(f"[OK] Correlation heatmap created")
        print(f"    Figure size: {fig.get_size_inches()}")
    else:
        print("[SKIP] Less than 2 numeric columns")
except Exception as e:
    print(f"[ERROR] Correlation heatmap: {e}")

print("\n[DONE] Charts produktcheck complete")
