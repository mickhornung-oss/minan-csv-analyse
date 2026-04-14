# Architektur - MinAn 1.4

## Grundprinzip

MinAn 1.4 folgt einer klaren Schichtentrennung: Die UI-Schicht ist von der Fachlogik getrennt. Services kapseln alle fachlichen Operationen. Der Session-State ist der zentrale Datenhaltungspunkt.

## Moduluebersicht

### domain/

Enthaelt die Kernmodelle der Anwendung:

- `session_state.py`: Zentrale Sitzungsverwaltung. Haelt Original-DataFrame und Arbeitskopie strikt getrennt.
- `models.py`: Datenklassen fuer Spaltenprofile, Datensatzprofile und Exportergebnisse.
- `enums.py`: Typen und Statuswerte.

### services/

Kapseln die Fachlogik unabhaengig von der UI:

- `import_service.py`: CSV laden mit Encoding- und Separator-Erkennung.
- `profile_service.py`: Strukturprofil erstellen.
- `quality_service.py`: Datenqualitaetspruefung.
- `chart_service.py`: Standarddiagramme erzeugen.
- `summary_service.py`: Textzusammenfassung erzeugen.
- `transform_service.py`: Bearbeitungen auf der Arbeitskopie.
- `export_service.py`: CSV-Export der aktiven Sicht.
- `report_service.py`: HTML-Bericht der aktiven Sicht.

### ui/

PySide6-basierte Desktop-Oberflaeche:

- `main_window.py`: Hauptfenster mit Toolbar und Tab-Navigation.
- `dialogs.py`: Datei-Dialoge, Hinweise und Schnellstart.
- `widgets/`: Einzelne Panels fuer Ueberblick, Tabelle, Kennzahlen, Diagramme, Bearbeiten und Export.
- `models/`: Qt-Table-Model-Adapter fuer pandas DataFrames.

### utils/

Hilfsfunktionen ohne Fachlogik:

- `csv_sniffer.py`
- `file_helpers.py`
- `text_helpers.py`
- `validators.py`

## Session-State-Konzept

Der `SessionState` ist das Zentrum der Datenhaltung:

1. Beim Laden wird der Original-DataFrame gespeichert und eine Arbeitskopie erzeugt.
2. Alle Analysen und Bearbeitungen laufen auf der Arbeitskopie.
3. Das Original bleibt unangetastet.
4. Exporte schreiben immer neue Dateien.
5. Ruecksetzen stellt den Originalzustand wieder her.

## Abhaengigkeitsrichtung

```text
UI -> Services -> Domain
UI -> Utils
Services -> Utils
```

Services kennen keine UI. Die UI ruft Services auf und stellt Ergebnisse dar.

## Konfiguration

Zentrale Konstanten fuer Produktname, Version, Defaults und portable Pfade liegen in `config.py`. Harte Benutzerpfade werden vermieden.
