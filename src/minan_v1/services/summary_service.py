"""Summary-Service: Regelbasierte Kurzzusammenfassung auf Deutsch."""

from minan_v1.domain.models import DatasetProfile, QualityReport, SummaryResult
from minan_v1.utils.text_helpers import format_number


def generate_summary(profile: DatasetProfile, quality: QualityReport) -> SummaryResult:
    """Erzeugt eine kompakte, priorisierte Kurzzusammenfassung des Datensatzes.

    Fokus auf die wichtigsten Befunde, max ~5-7 Sätze für große Datensätze.
    """
    lines: list[str] = []

    # --- 1. Datensatzgröße (Kontext) ---
    lines.append(
        f"Datensatz: {format_number(profile.row_count, 0)} Zeilen, {profile.column_count} Spalten "
        f"({profile.numeric_columns}N / {profile.categorical_columns}K / {profile.datetime_columns}D)."
    )

    # --- 2. Kritische Datenqualitäts-Probleme ---
    quality_issues = []

    # Duplikate - kritisch
    if quality.duplicate_rows > 0:
        pct = quality.duplicate_rows / profile.row_count * 100
        quality_issues.append(f"{quality.duplicate_rows} Duplikate ({pct:.1f}%)")

    # Hohe Fehlwertquoten - kritisch
    if quality.high_missing_columns:
        # Nur die problematischsten (~top 2)
        top_missing = sorted(
            quality.high_missing_columns, key=lambda x: x[1], reverse=True
        )[:2]
        for col_name, pct in top_missing:
            quality_issues.append(f"'{col_name}': {pct}% fehlend")

    # Leere Spalten - kritisch
    if quality.empty_columns:
        quality_issues.append(f"{len(quality.empty_columns)} leere Spalte(n)")

    if quality_issues:
        lines.append(f"Qualitätsprobleme: {', '.join(quality_issues)}.")
    else:
        lines.append("Keine kritischen Qualitätsprobleme gefunden.")

    # --- 3. Strukturelle Besonderheiten (optional, kompakt) ---
    structure_notes = []

    # Konstante Spalten
    if quality.constant_columns:
        structure_notes.append(f"{len(quality.constant_columns)} konstante")

    # Mögliche ID-Spalten
    id_cols = [c for c in profile.columns if c.is_id_like]
    if id_cols:
        structure_notes.append(f"{len(id_cols)} ID-ähnliche")

    if structure_notes:
        lines.append(f"Struktur: {', '.join(structure_notes)} Spalte(n).")

    # --- 4. Gesamtübersicht Fehlwerte ---
    if profile.total_missing > 0:
        total_cells = profile.row_count * profile.column_count
        pct = profile.total_missing / total_cells * 100 if total_cells > 0 else 0
        lines.append(
            f"Fehlwerte insgesamt: {format_number(profile.total_missing, 0)} ({pct:.1f}%)."
        )
    else:
        lines.append("Keine fehlenden Werte.")

    return SummaryResult(lines=lines)
