#!/usr/bin/env python3
"""Block-3 Produktcheck mit Stresstest-Datei."""

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
print("MinAn 1.4 BLOCK 3 - PRODUKTCHECK MIT STRESSTEST")
print("=" * 80)

print("\n[1/4] CSV-Datei laden...")
df, import_result = load_csv(csv_path)
if not import_result.success:
    print(f"[ERROR] CSV-Laden fehlgeschlagen: {import_result.error}")
    sys.exit(1)
print(f"[OK] Stresstest geladen: {df.shape[0]} Zeilen x {df.shape[1]} Spalten")

print("\n[2/4] Profil und Qualitaet berechnen...")
profile = create_profile(df)
quality = compute_quality_report(df, profile)
summary = generate_summary(profile, quality)
print("[OK] Profil erstellt")
print(
    f"     - Spalten: {profile.column_count} (Num: {profile.numeric_columns}, "
    f"Kat: {profile.categorical_columns}, Dat: {profile.datetime_columns})"
)
print(f"     - Fehlwerte: {profile.total_missing} gesamt")
print(f"     - Duplikate: {profile.duplicate_rows}")

print("\n[3/4] Qualitaets-Befunde analysieren...")
warnings = [f for f in quality.findings if f.severity in ("warning", "critical")]
hints = [f for f in quality.findings if f.severity == "info"]
print(f"[OK] Quality-Report: {len(quality.findings)} Findings")
print(f"     - Warnungen: {len(warnings)}")
print(f"     - Hinweise: {len(hints)}")

print("\n[4/4] Summary pruefen...")
print(f"[OK] Summary: {len(summary.lines)} Saetze")
for i, line in enumerate(summary.lines, 1):
    print(f"     {i}. {line}")

print("\n" + "=" * 80)
print("BLOCK 3 VALIDIERUNGEN")
print("=" * 80)

validations = []
validations.append(
    ("OK" if profile.column_count == df.shape[1] else "FAIL", f"Spaltenanzahl: {profile.column_count}")
)
validations.append(
    ("OK" if profile.row_count == len(df) else "FAIL", f"Zeilenanzahl: {profile.row_count}")
)
validations.append(
    ("OK" if len(summary.lines) <= 7 else "FAIL", f"Summary-Laenge: {len(summary.lines)}")
)
validations.append(
    ("OK" if profile.numeric_columns >= 1 else "FAIL", f"Numerische Spalten: {profile.numeric_columns}")
)

for status, message in validations:
    print(f"[{status}] {message}")

failed = [v for v in validations if v[0] != "OK"]
if failed:
    print(f"\n[FAIL] {len(failed)} Validierung(en) fehlgeschlagen")
    sys.exit(1)

print("\n[OK] Produktcheck abgeschlossen")
