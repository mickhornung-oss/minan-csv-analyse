# MinAn 1.4 - CSV-Schnellanalyse

Lokales, portables Windows-Desktop-Tool zur schnellen Analyse von CSV-Dateien.

## Projektziel

MinAn 1.4 laedt CSV-Dateien per Klick und liefert einen strukturierten Ueberblick: Strukturprofil, Datenqualitaet, Kennzahlen, Diagramme, Arbeitsansicht mit Filtern und Schnellansichten sowie lokale Weitergabe per CSV und HTML-Bericht. Die Originaldatei bleibt unveraendert.

## Stand 1.4

- CSV laden und direkt analysieren
- Arbeitsansicht mit Mehrfachfiltern, Schnellansichten und Typuebersteuerung
- Export der aktiven Sicht als neue CSV-Datei
- Lokaler HTML-Analysebericht aus der aktiven Sicht
- Info-/Schnellstart-Zugang mit Button fuer die mitgelieferte Beispieldatei
- Portable Release-Struktur mit `output` im Hauptordner und Beispieldatei unter `_internal/sample_data`
- Konsolidierter Build-/Release-Pfad auf `dist/MinAn_1_4`
- Aktueller Teststand: `155 passed` (lokal mit `pytest -q`)

## Portable Release-Struktur

```text
dist/MinAn_1_4/
|- MinAn.exe
|- _internal/
|  `- sample_data/
|     `- test_csv_deutsch_200x15.csv
|- output/
|  |- reports/
|  `- csv/
|- README_Kurzstart.txt
`- README.md
```

## Schnellstart

- `CSV oeffnen` fuer eigene Dateien
- `Info / Schnellstart` fuer kurze Nutzungshinweise
- `Beispieldatei laden` direkt aus `_internal/sample_data`
- HTML-Berichte landen standardmaessig in `output/reports`
- CSV-Exporte landen standardmaessig in `output/csv`

## Start im Dev-Modus

```batch
run_dev.bat
```

Voraussetzung:

```bash
pip install -r requirements.txt
```

## Release bauen

```batch
build_release.bat
```

Das Ergebnis liegt in `dist/MinAn_1_4/` und ist direkt portable nutzbar.

## Projektinterne Hilfsskripte

- Produktcheck- und Analysehilfen liegen unter `scripts/` (siehe `scripts/README.md`).
- Praesentationsskripte liegen unter `scripts/presentation/` und sind interne Begleitwerkzeuge (nicht Laufzeitkern).

## Produktnahe Smoke-Absicherung

- GUI-Hauptpfad (offscreen): `tests/test_product_smoke_gui.py`
- Deckt den Fluss Laden -> Tabs -> aktive Sicht -> CSV-Export -> HTML-Report ab.

## Version

- Release-Version: `1.4`
- Fokus: produktive Schnellstartfuehrung, portable Release-Ordnerlogik und lokaler HTML-Bericht
