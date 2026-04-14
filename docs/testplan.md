# Testplan - MinAn 1.4

## Zielplattform

- Windows 10/11
- Python 3.10+
- Pytest

## Automatisierte Testbereiche

### 1. CSV-Import

- CSV mit verschiedenen Encodings laden
- Separator-Erkennung pruefen
- Fehlerbehandlung bei ungueltigen Dateien
- Originaldatei bleibt unveraendert

### 2. Profilierung

- Zeilen- und Spaltenzahlen korrekt
- Typ-Erkennung korrekt
- Missing- und Unique-Werte korrekt

### 3. Datenqualitaet

- Missing-Erkennung
- Duplikat-Erkennung
- leere DataFrames als Grenzfall

### 4. Diagramme

- Histogramm, Balkendiagramm und weitere Standarddiagramme erzeugen Figure-Objekte
- robuste Behandlung ungueltiger oder leerer Eingaben

### 5. Transformationen

- Umbenennen, Loeschen, Ausblenden
- Filtern und Sortieren
- Schnellansichten
- Markierungen fuer Dubletten und Fehlwerte
- nur Arbeitskopie betroffen

### 6. Export und Bericht

- CSV-Export erzeugt neue Datei
- HTML-Bericht erzeugt neue Datei
- aktive Sicht bleibt konsistent
- Originaldatei wird nicht ueberschrieben

### 7. Session-State und Pfade

- Session-State trennt Original und Arbeitskopie
- portable Pfade fuer Output und Beispieldatei stimmen
- keine Nutzdaten in falschen Release-Bereichen

## Manuelle Smoke-Tests

| Test | Beschreibung |
|---|---|
| App startet | Fenster oeffnet korrekt |
| CSV laden | Datei wird geladen und analysiert |
| Ueberblick | Struktur und Hinweise werden angezeigt |
| Bearbeiten | Filter, Schnellansichten und Markierungen funktionieren |
| Bericht | HTML-Bericht aus aktiver Sicht wird erzeugt |
| Export | CSV aus aktiver Sicht wird erzeugt |
| Portable Startlogik | Release startet ohne Installation |
