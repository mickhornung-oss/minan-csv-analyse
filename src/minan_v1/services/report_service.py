"""Report-Service: Erzeugt lokale HTML-Berichte aus der aktiven Analyseansicht."""

from __future__ import annotations

import base64
import html
from datetime import datetime
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt

from minan_v1.config import APP_TITLE, APP_VERSION, REPORT_TITLE
from minan_v1.domain.enums import ColumnType
from minan_v1.domain.models import ReportChart, ReportResult
from minan_v1.domain.session_state import SessionState
from minan_v1.resources import ensure_runtime_dirs
from minan_v1.services.chart_service import (
    create_bar_chart,
    create_correlation_heatmap,
    create_histogram,
    create_missing_chart,
    get_categorical_columns,
    get_numeric_columns,
)


def build_report_filename(timestamp: datetime | None = None) -> str:
    """Erzeugt einen standardisierten Dateinamen fuer den HTML-Bericht."""
    ts = (timestamp or datetime.now()).strftime("%Y%m%d_%H%M%S")
    return f"MinAn_Bericht_{ts}.html"


def export_html_report(session: SessionState, target_path: Path) -> ReportResult:
    """Exportiert einen HTML-Bericht aus der aktuellen aktiven Sicht."""
    ensure_runtime_dirs()
    if not session.has_data or session.current_df is None:
        return ReportResult(
            success=False, error="Keine Daten fuer den Bericht vorhanden."
        )
    if (
        session.import_result is None
        or session.profile is None
        or session.quality_report is None
        or session.summary is None
    ):
        return ReportResult(success=False, error="Analysezustand ist unvollstaendig.")
    if target_path is None:
        return ReportResult(success=False, error="Kein Zielpfad angegeben.")
    if session.source_path and target_path == session.source_path:
        return ReportResult(
            success=False, error="Die Originaldatei darf nicht ueberschrieben werden."
        )

    if target_path.suffix.lower() != ".html":
        target_path = target_path.with_suffix(".html")
    target_path.parent.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now()
    charts = _build_report_charts(session)
    html_text = _render_html_report(session, created_at, charts)

    try:
        target_path.write_text(html_text, encoding="utf-8")
        return ReportResult(
            success=True,
            file_path=target_path,
            view_name=session.describe_active_view(),
            row_count=len(session.current_df),
            column_count=len(session.current_df.columns),
            charts=charts,
        )
    except PermissionError:
        return ReportResult(
            success=False,
            error=f"Keine Berechtigung zum Schreiben nach '{target_path}'.",
        )
    except Exception as exc:
        return ReportResult(success=False, error=f"Fehler beim Berichtsexport: {exc}")


def _build_report_charts(session: SessionState) -> list[ReportChart]:
    df = session.current_df
    profile = session.profile
    chart_specs: list[tuple[str, object]] = []

    missing_fig = create_missing_chart(df)
    if missing_fig is not None:
        chart_specs.append(("Fehlende Werte", missing_fig))

    numeric_columns = get_numeric_columns(profile)
    if numeric_columns:
        hist_fig = create_histogram(df, numeric_columns[0])
        chart_specs.append((f"Histogramm: {numeric_columns[0]}", hist_fig))

    correlation_fig = create_correlation_heatmap(df)
    if correlation_fig is not None:
        chart_specs.append(("Korrelationsmatrix", correlation_fig))
    else:
        categorical_columns = get_categorical_columns(profile)
        if categorical_columns:
            bar_fig = create_bar_chart(df, categorical_columns[0])
            chart_specs.append((f"Top-Kategorien: {categorical_columns[0]}", bar_fig))

    report_charts: list[ReportChart] = []
    for title, fig in chart_specs[:3]:
        report_charts.append(
            ReportChart(title=title, image_base64=_figure_to_base64(fig))
        )
    return report_charts


def _figure_to_base64(fig) -> str:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def _render_html_report(
    session: SessionState, created_at: datetime, charts: list[ReportChart]
) -> str:
    profile = session.profile
    quality = session.quality_report
    summary = session.summary
    import_result = session.import_result
    source_name = import_result.file_name or "Unbekannte CSV"
    active_filters = session.active_filter_texts()
    view_text = session.describe_active_view()

    warning_items = [
        finding.message
        for finding in quality.findings
        if finding.severity in ("warning", "critical")
    ]
    hint_items = [
        finding.message for finding in quality.findings if finding.severity == "info"
    ]
    numeric_columns = [
        c for c in profile.columns if c.column_type == ColumnType.NUMERIC
    ][:5]
    notable_columns = profile.columns[:8]

    charts_html = (
        "".join(
            [
                (
                    "<section class='chart-card'>"
                    f"<h3>{_esc(chart.title)}</h3>"
                    f"<img alt='{_esc(chart.title)}' src='data:image/png;base64,{chart.image_base64}' />"
                    "</section>"
                )
                for chart in charts
            ]
        )
        or "<p class='muted'>Fuer diese Sicht konnten keine Diagramm-Snapshots erzeugt werden.</p>"
    )

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_esc(REPORT_TITLE)}</title>
  <style>
    :root {{
      --bg: #f5f1e8;
      --card: #fffdf9;
      --ink: #1f2933;
      --muted: #5b6875;
      --accent: #264653;
      --accent-soft: #e4ecef;
      --warn: #b45309;
      --border: #d8d2c7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", Tahoma, sans-serif;
      color: var(--ink);
      background: linear-gradient(180deg, #f9f4ea 0%, var(--bg) 100%);
    }}
    .page {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 28px;
    }}
    .hero {{
      background: linear-gradient(135deg, var(--accent) 0%, #3f6c78 100%);
      color: white;
      border-radius: 20px;
      padding: 28px;
      box-shadow: 0 18px 40px rgba(38, 70, 83, 0.18);
    }}
    .hero h1 {{ margin: 0 0 8px 0; font-size: 30px; }}
    .hero p {{ margin: 6px 0; color: rgba(255,255,255,0.92); }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 18px;
      box-shadow: 0 10px 24px rgba(31, 41, 51, 0.06);
    }}
    h2 {{
      font-size: 18px;
      margin: 0 0 12px 0;
      color: var(--accent);
    }}
    h3 {{
      font-size: 15px;
      margin: 0 0 10px 0;
    }}
    .stat {{
      font-size: 28px;
      font-weight: 700;
      margin: 4px 0;
    }}
    .muted {{ color: var(--muted); }}
    ul {{
      margin: 0;
      padding-left: 18px;
    }}
    li {{ margin: 6px 0; }}
    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .chip {{
      display: inline-block;
      padding: 8px 12px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent);
      font-size: 13px;
      font-weight: 600;
    }}
    .chart-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}
    .chart-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px;
    }}
    .chart-card img {{
      display: block;
      width: 100%;
      height: auto;
      border-radius: 12px;
      border: 1px solid #e6e1d8;
      background: white;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      text-align: left;
      padding: 9px 10px;
      border-bottom: 1px solid #e9e4db;
      vertical-align: top;
    }}
    th {{ color: var(--accent); }}
    .note {{
      border-left: 4px solid var(--warn);
      padding-left: 12px;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <p>{_esc(APP_TITLE)} | Version {_esc(APP_VERSION)}</p>
      <h1>{_esc(REPORT_TITLE)}</h1>
      <p>Datei: {_esc(source_name)}</p>
      <p>Bericht erstellt am: {_esc(created_at.strftime("%d.%m.%Y %H:%M:%S"))}</p>
      <p>Aktive Sicht: {_esc(view_text)}</p>
    </section>

    <section class="grid">
      <article class="card">
        <h2>Aktive Sicht</h2>
        <div class="stat">{len(session.current_df)}</div>
        <p class="muted">Zeilen in der aktuell sichtbaren Analyseansicht</p>
      </article>
      <article class="card">
        <h2>Spalten</h2>
        <div class="stat">{len(session.current_df.columns)}</div>
        <p class="muted">Spalten in der Berichtssicht</p>
      </article>
      <article class="card">
        <h2>Fehlende Werte</h2>
        <div class="stat">{profile.total_missing}</div>
        <p class="muted">Fehlende Zellen in der aktiven Sicht</p>
      </article>
      <article class="card">
        <h2>Dubletten</h2>
        <div class="stat">{quality.duplicate_rows}</div>
        <p class="muted">Doppelte Zeilen in der aktiven Sicht</p>
      </article>
    </section>

    <section class="grid">
      <article class="card">
        <h2>Zusammenfassung</h2>
        <ul>{''.join(f'<li>{_esc(line)}</li>' for line in summary.lines)}</ul>
      </article>
      <article class="card">
        <h2>Aktive Filter und Modus</h2>
        <div class="chips">
          {''.join(f"<span class='chip'>{_esc(text)}</span>" for text in active_filters) or "<span class='chip'>Keine aktiven Filter</span>"}
          {"" if session.quick_view_mode is None else f"<span class='chip'>{_esc(view_text)}</span>"}
        </div>
        <p class="note">Der Bericht basiert auf der aktuellen Arbeitsansicht. Originaldatei und Originaldaten bleiben unveraendert.</p>
      </article>
      <article class="card">
        <h2>Typverteilung</h2>
        <ul>
          <li>Numerisch: {profile.numeric_columns}</li>
          <li>Kategorisch: {profile.categorical_columns}</li>
          <li>Datum: {profile.datetime_columns}</li>
          <li>ID: {profile.id_columns}</li>
          <li>Boolesch/Kurz kategorisch: {profile.boolean_columns}</li>
        </ul>
      </article>
    </section>

    <section class="grid">
      <article class="card">
        <h2>Zentrale Datenqualitaetsbefunde</h2>
        <ul>{''.join(f'<li>{_esc(item)}</li>' for item in warning_items[:8]) or "<li>Keine Warnungen in der aktiven Sicht.</li>"}</ul>
      </article>
      <article class="card">
        <h2>Hinweise</h2>
        <ul>{''.join(f'<li>{_esc(item)}</li>' for item in hint_items[:8]) or "<li>Keine weiteren Hinweise in der aktiven Sicht.</li>"}</ul>
      </article>
    </section>

    <section class="card">
      <h2>Zentrale Kennzahlen</h2>
      <table>
        <thead>
          <tr>
            <th>Spalte</th>
            <th>Typ</th>
            <th>Gueltig</th>
            <th>Fehlend</th>
            <th>Mittelwert</th>
            <th>Median</th>
            <th>Min</th>
            <th>Max</th>
          </tr>
        </thead>
        <tbody>
          {''.join(_render_metric_row(column) for column in numeric_columns) or "<tr><td colspan='8'>Keine numerischen Kennzahlen in der aktiven Sicht vorhanden.</td></tr>"}
        </tbody>
      </table>
    </section>

    <section class="card">
      <h2>Auffaellige Spalten</h2>
      <table>
        <thead>
          <tr>
            <th>Spalte</th>
            <th>Erkannter Typ</th>
            <th>Fehlend</th>
            <th>Unique</th>
            <th>Top-Werte</th>
          </tr>
        </thead>
        <tbody>
          {''.join(_render_column_row(column) for column in notable_columns)}
        </tbody>
      </table>
    </section>

    <section>
      <h2>Diagramm-Snapshots</h2>
      <div class="chart-grid">{charts_html}</div>
    </section>
  </div>
</body>
</html>"""


def _render_metric_row(column) -> str:
    return (
        "<tr>"
        f"<td>{_esc(column.name)}</td>"
        f"<td>{_esc(column.column_type.name)}</td>"
        f"<td>{column.count}</td>"
        f"<td>{column.missing}</td>"
        f"<td>{_fmt(column.mean)}</td>"
        f"<td>{_fmt(column.median)}</td>"
        f"<td>{_fmt(column.min_val)}</td>"
        f"<td>{_fmt(column.max_val)}</td>"
        "</tr>"
    )


def _render_column_row(column) -> str:
    top_values = (
        ", ".join([f"{name} ({count})" for name, count in column.top_values[:3]]) or "-"
    )
    return (
        "<tr>"
        f"<td>{_esc(column.name)}</td>"
        f"<td>{_esc(column.column_type.name)}</td>"
        f"<td>{column.missing}</td>"
        f"<td>{column.unique}</td>"
        f"<td>{_esc(top_values)}</td>"
        "</tr>"
    )


def _fmt(value) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def _esc(value: str) -> str:
    return html.escape(str(value))
