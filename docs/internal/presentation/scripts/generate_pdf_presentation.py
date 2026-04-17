#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MinAn V1 PDF-PrÃ¤sentation Generator mit ReportLab
Erstellt eine PDF mit 8 Folien aus Projektdokumentation.
"""

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
from pathlib import Path

# Projekt-Verzeichnis
project_dir = str(Path(__file__).resolve().parents[4])
presentation_dir = os.path.join(project_dir, "docs", "internal", "presentation")

# Verzeichnis erstellen, falls nicht vorhanden
os.makedirs(presentation_dir, exist_ok=True)

pdf_path = os.path.join(presentation_dir, "MinAn_1_4_Abschlusspraesentation.pdf")

# PDF mit ReportLab erstellen
class PDFSlide:
    def __init__(self, path):
        self.path = path
        self.slides = []

    def add_slide(self, title, content_lines, title_bg_color=None):
        """Folie hinzufÃ¼gen"""
        self.slides.append({
            'title': title,
            'content': content_lines,
            'title_bg': title_bg_color or '#217B9B'
        })

    def generate(self):
        """PDF erzeugen"""
        c = canvas.Canvas(self.path, pagesize=landscape(A4))
        width, height = landscape(A4)

        for slide_num, slide in enumerate(self.slides):
            # Hintergrund
            c.setFillColorRGB(1, 1, 1)  # Weiss
            c.rect(0, 0, width, height, fill=1, stroke=0)

            # Titel-Balken
            self._draw_title_bar(c, slide['title'], width, height)

            # Inhalte
            self._draw_content(c, slide['content'], width, height)

            # Footer mit Foliennummer
            c.setFont("Helvetica", 10)
            c.drawString(width - 1*inch, 0.2*inch, "Folie {}".format(slide_num + 1))

            # Neue Seite
            if slide_num < len(self.slides) - 1:
                c.showPage()

        c.save()

    def _draw_title_bar(self, c, title, width, height):
        """Titel-Balken zeichnen"""
        # Hintergrund
        c.setFillColorRGB(0.13, 0.46, 0.61)  # Dunkelblau (#217B9B)
        c.rect(0, height - 1*inch, width, 1*inch, fill=1, stroke=0)

        # Text
        c.setFont("Helvetica-Bold", 32)
        c.setFillColorRGB(1, 1, 1)  # Weiss
        c.drawString(0.4*inch, height - 0.6*inch, title)

    def _draw_content(self, c, content_lines, width, height):
        """Inhalte zeichnen"""
        y_pos = height - 1.4*inch
        c.setFont("Helvetica", 14)
        c.setFillColorRGB(0.2, 0.2, 0.2)  # Dunkelgrau

        line_height = 0.25*inch

        for line in content_lines:
            if line.strip() == "":  # Leere Zeile
                y_pos -= line_height / 2
            else:
                # Text umbrechen, wenn zu lang
                if len(line) > 80:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line) + len(word) > 75:
                            c.drawString(0.6*inch, y_pos, current_line.strip())
                            y_pos -= line_height
                            current_line = word
                        else:
                            current_line += " " + word
                    if current_line.strip():
                        c.drawString(0.6*inch, y_pos, current_line.strip())
                else:
                    c.drawString(0.6*inch, y_pos, line)
                y_pos -= line_height

# PrÃ¤sentation erstellen
pdf = PDFSlide(pdf_path)

# FOLIE 1: Titel
pdf.add_slide("MinAn V1", [
    "",
    "Portables Windows-Tool zur lokalen CSV-Schnellanalyse",
    "",
    "Version 1.0.0"
])

# FOLIE 2: Problem und Ziel
pdf.add_slide("Problem und Ziel", [
    "Problem: CSV-Dateien schnell und lokal analysieren",
    "Anforderung: Originaldatei muss unverÃ¤ndert bleiben",
    "",
    "Ziele von MinAn V1:",
    "  - Lokal, schnell, verstÃ¤ndlich",
    "  - Portable Nutzung ohne Pflichtinstallation",
    "  - Windows-Desktop-Tool fuer sofortige Analyse"
])

# FOLIE 3: Funktionsumfang V1
pdf.add_slide("Funktionsumfang V1", [
    "CSV laden mit Auto-Encoding/Separator-Erkennung",
    "",
    "Ueberblick: Strukturprofil, Datenqualitaet, Kennzahlen",
    "",
    "Diagramme: Histogramme, Balkendiagramme, Boxplots",
    "",
    "Bearbeitung auf Arbeitskopie: Spalten, Filter, Sortierung",
    "",
    "Export: Bearbeitete Daten als neue CSV-Datei"
])

# FOLIE 4: Architektur
pdf.add_slide("Architektur & Datenschutz", [
    "Session-State: Original + Arbeitskopie strikt getrennt",
    "",
    "Services-Layer: CSV-Import, Profil, Qualitaet, Diagramme, Export",
    "",
    "UI-Schicht: PySide6, unabhaengig von Geschaeftslogik",
    "",
    "Schutzregel: Originaldatei wird NIEMALS veraendert",
    "",
    "Workflow: Laden -> Analysieren -> Bearbeiten -> Exportieren"
])

# FOLIE 5: BenutzeroberflÃ¤che
pdf.add_slide("Benutzeroberflaeche", [
    "Tab-Navigation:",
    "  - Ueberblick | Tabelle | Kennzahlen | Diagramme | Bearbeitung | Export",
    "",
    "Ueberblick-Tab: Dateiinfo, Strukturprofil, Qualitaetsbericht",
    "",
    "Tabellen-Tab: Scrollbare Vorschau mit Paginierung",
    "",
    "Kennzahlen-Tab: Mean, Median, Std, Min, Max pro Spalte"
])

# FOLIE 6: QualitÃ¤tssicherung
pdf.add_slide("Qualitaetssicherung", [
    "75/75 Unit-Tests erfolgreich (100%)",
    "",
    "Automatisierte Smoke-Tests erfolgreich",
    "",
    "Datenschutz validiert: Original nach Import unveraendert",
    "",
    "Deutsche Test-CSV validiert (7 Spalten, Typklassifikation korrekt)",
    "",
    "Automatische Encoding/Separator-Erkennung getestet"
])

# FOLIE 7: Release & PortabilitÃ¤t
pdf.add_slide("Release & Portabilitaet", [
    "One-Folder-Release: dist/MinAn_1_4/",
    "",
    "MinAn.exe (ca. 10 MB) - Startdatei, kein Installer noetig",
    "",
    "Python-Runtime enthalten, keine Installation erforderlich",
    "",
    "Portable Nutzung: Funktioniert direkt nach dem Entpacken",
    "",
    "USB-Stick-faehig: Gesamter Ordner ist portabel einsetzbar"
])

# FOLIE 8: Fazit
pdf.add_slide("Fazit", [
    "MinAn V1 erfolgreich abgeschlossen und releasebereit",
    "",
    "Alle Kernziele erreicht:",
    "  - Lokal, schnell, portable, sichere Datenbehandlung",
    "",
    "Umfassend getestet:",
    "  - 75 Unit-Tests, Smoke-Tests, Produktvalidierung",
    "",
    "Einsatzbereit als Windows-Desktop-Tool fuer schnelle CSV-Analyse"
])

# PDF erzeugen
pdf.generate()
print("[OK] PDF erstellt: {}".format(pdf_path))
print("PraesentationsenthÃ¤lt 8 Folien (deutsch, Landscape A4)")

