# Analyse-Umfang - MinAn 1.4

## Verbindlicher Standardanalyse-Umfang

MinAn 1.4 liefert nach dem Laden einer CSV-Datei automatisch folgende Analysen:

## 1. Strukturprofil

| Metrik | Beschreibung |
|---|---|
| Zeilen / Spalten | Dimensionen des Datensatzes |
| Spaltentypen | Numerisch, Kategorisch, Datum, Text |
| Encoding | Erkanntes Datei-Encoding |
| Separator | Erkanntes Trennzeichen |
| Dateigroesse | Groesse der Quelldatei |

## 2. Datenqualitaet

| Pruefung | Beschreibung |
|---|---|
| Missing Values | Anzahl und Anteil pro Spalte |
| Duplikate | Anzahl vollstaendig doppelter Zeilen |
| Unique Values | Anzahl eindeutiger Werte pro Spalte |
| Typmix-Warnung | Hinweis bei gemischten Typen in einer Spalte |

## 3. Standardkennzahlen

- Count (gueltige Werte)
- Mean (Durchschnitt)
- Median
- Standardabweichung
- Minimum / Maximum
- Top-N haeufigste Werte fuer kategorische Spalten

## 4. Diagramm-Grundpaket

| Diagramm | Einsatz |
|---|---|
| Histogramm | Verteilung numerischer Spalten |
| Balkendiagramm | Haeufigkeit kategorischer Spalten |
| Boxplot | Verteilung und Ausreisser numerischer Spalten |
| Korrelationsmatrix | Zusammenhaenge zwischen numerischen Spalten |

Jedes Diagramm wird automatisch fuer geeignete Spalten angeboten. Nutzer koennen Spalten zur Darstellung auswaehlen.

## 5. Bearbeitungsfunktionen

| Funktion | Einsatz |
|---|---|
| Spalten umbenennen | Aendern von Spaltennamen |
| Spalten entfernen | Loeschen von Spalten aus der Arbeitskopie |
| Spalten ausblenden | Visuelles Ausblenden von Spalten |
| Filter | Einfache Filter fuer numerische und kategoriale Spalten |
| Sortierung | Aufsteigend oder absteigend nach Spalten |
| Dubletten markieren | Markierung doppelter Zeilen |
| Fehlende Werte markieren | Markierung fehlender Werte |

Alle Bearbeitungen erfolgen auf einer internen Arbeitskopie. Die Originaldatei bleibt unveraendert.

## 6. Export

| Funktion | Einsatz |
|---|---|
| CSV exportieren | Speichern der aktiven Sicht als neue CSV-Datei |
| HTML-Bericht exportieren | Bericht aus der aktiven Sicht erzeugen |

Der Export erzeugt immer neue Dateien und ueberschreibt niemals die Originaldatei.

## 7. Kurzzusammenfassung

Nach Abschluss der Analyse wird eine lesbare Kurzzusammenfassung erzeugt, die Dimensionen, Qualitaetshinweise und auffaellige Kennzahlen auf einen Blick darstellt.

## Nicht im Scope

- Komplexe statistische Tests
- Zeitreihenanalysen
- Machine-Learning-basierte Auswertungen
- Freie Diagramm-Konfiguration
- Automatische Datenbereinigung oder Imputation
