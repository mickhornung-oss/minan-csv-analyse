"""Qualitaets-Service: Datenqualitaetsmetriken und priorisierte Auffaelligkeiten."""

import pandas as pd

from minan_v1.config import MAX_UNIQUE_VALUES_FOR_CATEGORICAL
from minan_v1.domain.models import QualityFinding, QualityReport
from minan_v1.services.column_type_service import classify_column, is_id_column

HIGH_MISSING_PCT = 30.0
NEAR_CONSTANT_PCT = 99.0
HIGH_CARDINALITY_FACTOR = 0.9

_SEVERITY_ORDER = {"critical": 0, "warning": 1, "info": 2}
_CATEGORY_ORDER = {
    "Duplikate": 0,
    "Struktur": 1,
    "Leere Spalte": 2,
    "Fehlwerte": 3,
    "Konstante Spalte": 4,
    "Nahezu konstant": 5,
    "Hohe Kardinalitaet": 6,
}


def compute_quality_report(df: pd.DataFrame, profile=None) -> QualityReport:
    """Berechnet Qualitaetskennzahlen und priorisierte Findings."""
    report = QualityReport()
    total_rows = len(df)

    if total_rows == 0:
        report.findings.append(
            QualityFinding(
                category="Struktur",
                severity="critical",
                message="Der Datensatz enthaelt keine Zeilen.",
            )
        )
        return report

    findings: list[QualityFinding] = []

    report.duplicate_rows = int(df.duplicated().sum())
    if report.duplicate_rows > 0:
        pct = report.duplicate_rows / total_rows * 100
        findings.append(
            QualityFinding(
                category="Duplikate",
                severity="warning",
                message=f"{report.duplicate_rows} doppelte Zeilen ({pct:.1f}%).",
            )
        )

    report.empty_rows = int(df.isna().all(axis=1).sum())
    if report.empty_rows > 0:
        findings.append(
            QualityFinding(
                category="Struktur",
                severity="warning",
                message=f"{report.empty_rows} komplett leere Zeilen.",
            )
        )

    for col_name in df.columns:
        col = df[col_name]
        missing = int(col.isna().sum())
        missing_pct = missing / total_rows * 100

        if missing == total_rows:
            report.empty_columns.append(col_name)
            findings.append(
                QualityFinding(
                    category="Leere Spalte",
                    severity="critical",
                    message=f"Spalte '{col_name}' ist komplett leer.",
                    column=col_name,
                )
            )
            continue

        if missing_pct >= HIGH_MISSING_PCT:
            report.high_missing_columns.append((col_name, round(missing_pct, 1)))
            findings.append(
                QualityFinding(
                    category="Fehlwerte",
                    severity="warning",
                    message=f"Spalte '{col_name}': {missing_pct:.1f}% fehlende Werte.",
                    column=col_name,
                )
            )

        unique = col.nunique(dropna=True)
        if unique <= 1 and missing < total_rows:
            report.constant_columns.append(col_name)
            findings.append(
                QualityFinding(
                    category="Konstante Spalte",
                    severity="info",
                    message=f"Spalte '{col_name}' enthaelt nur einen Wert.",
                    column=col_name,
                )
            )
        elif unique > 1:
            top_freq = col.value_counts(dropna=True).iloc[0]
            non_missing = total_rows - missing
            top_pct = top_freq / non_missing * 100 if non_missing > 0 else 0
            if top_pct >= NEAR_CONSTANT_PCT:
                findings.append(
                    QualityFinding(
                        category="Nahezu konstant",
                        severity="info",
                        message=f"Spalte '{col_name}': Ein Wert dominiert mit {top_pct:.1f}%.",
                        column=col_name,
                    )
                )

        if unique > MAX_UNIQUE_VALUES_FOR_CATEGORICAL:
            non_missing = total_rows - missing
            if non_missing > 0 and unique / non_missing >= HIGH_CARDINALITY_FACTOR:
                report.high_cardinality_columns.append((col_name, unique))
                col_type = classify_column(col)
                if is_id_column(col, col_type, unique, total_rows):
                    findings.append(
                        QualityFinding(
                            category="Hohe Kardinalitaet",
                            severity="info",
                            message=f"Spalte '{col_name}': {unique} eindeutige Werte (moeglicherweise ID-Spalte).",
                            column=col_name,
                        )
                    )

    report.findings.extend(_sort_findings(findings))
    return report


def _sort_findings(findings: list[QualityFinding]) -> list[QualityFinding]:
    """Sortiert Findings stabil nach Severity und fachlicher Prioritaet."""
    return sorted(
        findings,
        key=lambda f: (
            _SEVERITY_ORDER.get(f.severity, 99),
            _CATEGORY_ORDER.get(f.category, 99),
            f.column or "",
            f.message,
        ),
    )
