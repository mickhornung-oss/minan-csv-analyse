# Benutzerhandbuch - MinAn 1.4

## Tool starten

**Entwicklungsmodus:**
Doppelklick auf `run_dev.bat`.

**Release-Version:**
Doppelklick auf `dist/MinAn_1_4/MinAn.exe`.

Die Anwendung ist portable. Alle sichtbaren Nutzdaten bleiben im Release-Hauptordner.

## Schnellstart

Oben sichtbar:

- `CSV oeffnen`
- `Bericht exportieren`
- `Info / Schnellstart`

Im Schnellstart finden Sie:

- kurze Erklaerung des Tools
- kompakte Nutzungsschritte
- Button `Beispieldatei laden`

Die Beispieldatei wird intern aus `_internal/sample_data` geladen.

## Eigene CSV laden

1. `CSV oeffnen` waehlen.
2. Datei auswaehlen.
3. Ueberblick, Kennzahlen, Diagramme und Tabelle pruefen.

## Aktive Sicht bearbeiten

Im Tab **Bearbeiten** koennen Sie:

- mehrere Filter setzen
- einzelne Filter entfernen oder alle zuruecksetzen
- Schnellansichten fuer fehlende Werte, Dubletten und Ausreisser-Kandidaten nutzen
- jederzeit zur Gesamtansicht zurueckkehren

Alle Zahlen in Tabelle, Kennzahlen, Diagrammen, Export und Bericht beziehen sich auf dieselbe aktive Sicht.

## Standard-Ausgabeordner

Im Release-Hauptordner werden automatisch angelegt:

- `output/reports` fuer HTML-Berichte
- `output/csv` fuer CSV-Exporte

Es werden keine Nutzdaten in `_internal` gespeichert.

## HTML-Bericht

Der HTML-Bericht dokumentiert die aktuelle aktive Sicht inklusive:

- Summary
- Datenqualitaetsbefunde
- Typverteilung
- aktive Filter oder Schnellansicht
- zentrale Kennzahlen
- Diagramm-Snapshots

Standardziel: `output/reports`

## CSV-Export

Die aktuelle aktive Sicht kann als neue CSV gespeichert werden.

Standardziel: `output/csv`

Die Originaldatei wird nicht ueberschrieben.
