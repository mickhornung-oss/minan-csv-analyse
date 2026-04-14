#!/usr/bin/env python3
"""Block-3 Stresstest-Analyse fuer Ueberblick, Summary und Findings."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from minan_v1.services.import_service import load_csv  # noqa: E402
from minan_v1.services.profile_service import create_profile  # noqa: E402
from minan_v1.services.quality_service import compute_quality_report  # noqa: E402
from minan_v1.services.summary_service import generate_summary  # noqa: E402

project_root = Path(__file__).resolve().parent.parent
csv_path = project_root / "assets" / "sample_data" / "stresstest_5000x19.csv"

print("=" * 80)
print("MinAn 1.4 BLOCK 3 - UEBERBLICK / SUMMARY / BERICHT UNTER STRESSTEST")
print("=" * 80)

print("\n[SCHRITT 1] CSV-Datei laden...")
df, import_result = load_csv(csv_path)
if not import_result.success:
    print(f"[ERROR] CSV-Laden fehlgeschlagen: {import_result.error}")
    sys.exit(1)

print(f"[OK] Stresstest geladen: {df.shape[0]} Zeilen x {df.shape[1]} Spalten")

print("\n[SCHRITT 2] Profil erstellen...")
profile = create_profile(df)
print("[OK] Profil erstellt")
print(f"     - Numerisch: {profile.numeric_columns}")
print(f"     - Kategorisch: {profile.categorical_columns}")
print(f"     - Datetime: {profile.datetime_columns}")
print(f"     - ID-aehnlich: {profile.id_columns}")

print("\n[SCHRITT 3] Quality-Report erstellen...")
quality = compute_quality_report(df, profile)
warnings = [f for f in quality.findings if f.severity in ("warning", "critical")]
hints = [f for f in quality.findings if f.severity == "info"]
print(f"[OK] Findings: {len(quality.findings)}")
print(f"     - Warnungen: {len(warnings)}")
print(f"     - Hinweise: {len(hints)}")

print("\n[SCHRITT 4] Summary...")
summary = generate_summary(profile, quality)
for i, line in enumerate(summary.lines, 1):
    print(f"{i}. {line}")

print("\nABSCHLUSS: Stresstest-Analyse fertig")
