#!/usr/bin/env python3
"""
Erstelle PDF aus PowerPoint-Inhalten mit ReportLab
"""

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from pathlib import Path

# Farben
COLOR_DARK = HexColor('#192328')
COLOR_GREEN = HexColor('#4CAF50')
COLOR_LIGHT = HexColor('#E6ECF0')

# Dokument-Setup
PROJECT_ROOT = Path(__file__).resolve().parents[2]
output_path = PROJECT_ROOT / "presentation" / "MinAn_1_4_Abschlusspraesentation.pdf"
doc = SimpleDocTemplate(
    str(output_path),
    pagesize=landscape(A4),
    topMargin=0.5*cm,
    bottomMargin=0.5*cm,
    leftMargin=0.8*cm,
    rightMargin=0.8*cm
)

# Styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=44,
    textColor=COLOR_GREEN,
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=32,
    textColor=COLOR_GREEN,
    spaceAfter=12,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontSize=12,
    textColor=COLOR_LIGHT,
    spaceAfter=8,
    leading=14
)

# Story für Inhalte
story = []

# Helper-Funktionen
def add_title_slide(title, subtitle):
    story.append(Spacer(1*cm, 1.5*cm))
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1*cm, 0.3*cm))
    story.append(Paragraph(subtitle, body_style))
    story.append(PageBreak())

def add_content_slide(title, content_list):
    story.append(Paragraph(title, heading_style))
    story.append(Spacer(1*cm, 0.3*cm))

    for item in content_list:
        story.append(Paragraph(f"• {item}", body_style))

    story.append(PageBreak())

# ============================================================================
# FOLIEN
# ============================================================================

# 1. TITELFOLIE
add_title_slide(
    "MinAn 1.4",
    "CSV-Schnellanalyse<br/>Lokales, portables Windows-Tool zur schnellen Analyse und Bearbeitung von CSV-Dateien"
)

# 2. AUSGANGSLAGE
add_content_slide(
    "Ausgangslage",
    [
        "Manuelle CSV-Erstanalyse ist zeitintensiv",
        "Unstrukturierter Überblick: Struktur, Qualität, Ausreißer",
        "Keine lokale, portable Lösung ohne Installation",
        "Cloud-Abhängigkeit oft nicht gewünscht",
        "Originaldatei muss geschützt sein",
        "Lösung: Schneller, lokaler, offline Überblick"
    ]
)

# 3. PRODUKTZIEL
add_content_slide(
    "Produktziel",
    [
        "Schneller Überblick ohne Setup",
        "Vollständig portabel und lokal",
        "Originaldatei geschützt",
        "Arbeitsfluss für Analysten: Laden → Prüfen → Bearbeiten → Export",
        "Fokus auf Fachlichkeit, nicht Komplexität",
        "Windows-nativer Desktop-Workflow"
    ]
)

# 4. FUNKTIONSUMFANG
add_content_slide(
    "Funktionsumfang",
    [
        "<b>CSV-Verwaltung:</b> CSV laden mit automatischer Encoding/Separator-Erkennung, Beispieldatei",
        "<b>Analyse & Vorschau:</b> Strukturprofil, Datenqualität, Kennzahlen, Diagramme, Tabellenansicht",
        "<b>Arbeitstools:</b> Mehrfach-Filter, Schnellansichten, Spalten-Bearbeitung",
        "<b>Export:</b> CSV-Export und HTML-Bericht (aktive Sicht)"
    ]
)

# 5. PRODUKTLOGIK
add_content_slide(
    "Produktlogik & Schutzkonzept",
    [
        "<b>Original → Arbeitskopie:</b> Originaldatei wird beim Laden gespeichert, alle Änderungen nur auf Arbeitskopie",
        "<b>Aktive Sicht:</b> Filter und Transformationen definieren aktive Sicht, Kennzahlen beziehen sich darauf",
        "<b>Export & Bericht:</b> CSV-Export speichert aktive Sicht als neue Datei, HTML-Bericht dokumentiert aktive Sicht",
        "<b>Schutz:</b> Originaldatei wird nie verändert oder überschrieben"
    ]
)

# 6. OBERFLÄCHE
add_content_slide(
    "Produktoberfläche",
    [
        "<b>Toolbar:</b> CSV öffnen, Bericht exportieren, Info/Schnellstart",
        "<b>Tabs:</b> Überblick, Kennzahlen, Diagramme, Tabelle, Bearbeiten, Export",
        "<b>Design:</b> Dunkles Modern-Design mit grünen Akzenten",
        "<b>Responsive Layouts:</b> für große und kleine Dateien"
    ]
)

# 7. TECHNIK-STACK
add_content_slide(
    "Technik-Stack",
    [
        "<b>Programmiersprache:</b> Python 3.10+",
        "<b>UI-Framework:</b> PySide6 (Qt6 für Python)",
        "<b>Datenverwaltung:</b> pandas (DataFrames), numpy (numerische Berechnung)",
        "<b>Visualisierung:</b> matplotlib (Diagramme, Charts)",
        "<b>Qualitätssicherung:</b> pytest (automatisierte Tests)"
    ]
)

# 8. BUILD & RELEASE
add_content_slide(
    "Build & Release",
    [
        "<b>Packaging:</b> PyInstaller One-Folder-Release → MinAn_1_4/ Ordner (portable)",
        "<b>Release-Struktur:</b> MinAn.exe, _internal/ (Python Runtime), output/ (Berichte/CSV), sample_data/",
        "<b>Versionierung:</b> Windows Version Info: 1.4.0.0, Productname: MinAn 1.4 - CSV-Schnellanalyse"
    ]
)

# 9. ARCHITEKTUR
add_content_slide(
    "Projektarchitektur",
    [
        "<b>UI-Layer:</b> main_window, dialogs, widgets, Qt-Models",
        "<b>Services:</b> import, profile, quality, chart, transform, export, report",
        "<b>SessionState & Domain:</b> original_df, working_df, filters & views, Models",
        "<b>Abhängigkeitsrichtung:</b> UI → Services → Domain; Services kennen keine UI"
    ]
)

# 10. QUALITÄTSSICHERUNG
add_content_slide(
    "Qualitätssicherung",
    [
        "<b>Automatisierte Tests:</b> 44+ Pytest-Tests für Import, Profiling, Qualität, Transformationen, Export",
        "<b>Test-Bereiche:</b> CSV-Import, Profilierung, Datenqualität, Diagramme, Transformationen, Session-State",
        "<b>Manuelle Smoke-Tests:</b> App startet, CSV laden, Tabs funktionieren, Export/Bericht funktionieren",
        "<b>Originalschutz:</b> Tests prüfen Schutz von original_df"
    ]
)

# 11. RELEASE & PORTABILITÄT
add_content_slide(
    "Release & Portabilität",
    [
        "<b>One-Folder-Prinzip:</b> dist/MinAn_1_4/ ist vollständig portabel, keine Systeminstallation",
        "<b>Ausgabeordner:</b> output/reports/ (HTML), output/csv/ (CSV-Exporte)",
        "<b>Beispieldatei:</b> test_csv_deutsch_200x15.csv (200 Zeilen, 15 Spalten) für Schnellstart",
        "<b>Schnellstart:</b> Info-Dialog mit Beispieldatei-Button"
    ]
)

# 12. PRODUKTREIFE & FEINSCHLIFF
add_content_slide(
    "Produktreife - Feinschliff",
    [
        "<b>UI/UX Politur:</b> Dark Mode, grüne Akzente, responsive Layouts, klare Toolbar, Info-Dialog",
        "<b>Produktmetadaten:</b> Produktname MinAn 1.4, Company MinAn Software, ModernGreen Icon",
        "<b>Fertigstellung 1.4:</b> Alle Tests grün, Release-Build erfolgreich, portable EXE lauffähig"
    ]
)

# 13. FAZIT
add_content_slide(
    "Fazit",
    [
        "<b>Was ist MinAn 1.4?</b> Ein reifes, produktives Analysewerkzeug für CSV-Daten",
        "<b>Kernstärken:</b> Lokal, portabel, sicher • Schneller Überblick • Originalschutz • Professioneller Export",
        "<b>Projektstand:</b> Version 1.4 ist Abschluss von Blocks 1-2, produktionsreif, bereit für Einsatz"
    ]
)

# Baue PDF
try:
    doc.build(story)
    print(f"[OK] PDF erfolgreich erstellt: {output_path}")
    print(f"[OK] Datei: {output_path.resolve()}")
    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024*1024)
        print(f"[OK] Größe: {size_mb:.2f} MB")
except Exception as e:
    print(f"[ERROR] Fehler beim Erstellen der PDF: {e}")
    import traceback
    traceback.print_exc()
