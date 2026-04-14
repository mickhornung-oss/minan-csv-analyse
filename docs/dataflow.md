# Datenfluss - MinAn 1.4

## Grundprinzip

Die Originaldatei wird niemals direkt veraendert. Alle Operationen laufen auf einer internen Arbeitskopie. Export und Bericht erzeugen immer neue Dateien.

## Fluss im Detail

```text
CSV-Datei -> import_service -> Original-DF -> Arbeitskopie
Arbeitskopie -> Analyse
Arbeitskopie -> Bearbeiten
Arbeitskopie -> CSV-Export / HTML-Bericht
```

## Schutzregeln

1. Die Originaldatei wird nur gelesen.
2. Der Original-DataFrame bleibt als Snapshot erhalten.
3. Die Arbeitskopie wird mit `df.copy()` erzeugt.
4. Exporte schreiben immer in neue Dateien.
5. Ruecksetzen stellt die Arbeitskopie aus dem Original wieder her.

## Beteiligte Komponenten

| Schritt | Komponente |
|---|---|
| CSV lesen | `import_service` |
| Arbeitskopie erzeugen | `SessionState.load()` |
| Analyse | `profile_service`, `quality_service`, `chart_service`, `summary_service` |
| Bearbeitung | `transform_service` |
| Export | `export_service`, `report_service` |
