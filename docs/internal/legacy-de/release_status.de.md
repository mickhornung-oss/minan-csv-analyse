# Release-Status - MinAn 1.4

## Status

MinAn 1.4 ist als portabler Release-Stand abgeschlossen.
Der konsolidierte Projektstand ist versions- und releasekonsistent auf `1.4`.
Freeze-Kandidat: Build-, Test- und Produktsmoke-Pfade sind verifiziert.

## Release-Ziel

- sichtbare Produktbezeichnung: `MinAn 1.4 - CSV-Schnellanalyse`
- portable One-Folder-Auslieferung
- lokale Analyse ohne Cloud-Abhaengigkeit
- HTML-Bericht und CSV-Export aus der aktiven Sicht

## Produktstand

- Schnellstart mit Beispieldatei
- Ueberblick, Kennzahlen, Diagramme, Tabelle, Bearbeiten und Export
- Mehrfachfilter, Schnellansichten und manuelle Typuebersteuerung
- kompakter HTML-Bericht aus der aktiven Sicht
- sichtbare Ausgabeordner fuer Berichte und CSV-Dateien
- final geglaetteter Bearbeiten-Tab mit klaren Markierungs-Toggles

## Release-Ordner

```text
dist/MinAn_1_4/
|- MinAn.exe
|- _internal/
|  `- sample_data/
|     `- test_csv_deutsch_200x15.csv
|- output/
|  |- reports/
|  `- csv/
`- README_Kurzstart.txt
```

## Freigabekriterien

- finaler Build erfolgreich
- EXE startet
- produktrelevante Tests erfolgreich (`pytest -q`: 155 passed)
- produktnaher GUI-Smoke erfolgreich (`test_product_smoke_gui.py`)
- keine bekannte Abhaengigkeit von `tests\...` im Release
- keine Nutzdaten ausser der mitgelieferten Beispieldatei in `_internal`
- sichtbare Release-Version konsistent auf `1.4`
