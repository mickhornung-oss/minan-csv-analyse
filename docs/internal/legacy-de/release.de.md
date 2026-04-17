# Release - MinAn 1.4

## Release-Konzept

MinAn 1.4 wird als portables Windows-Desktop-Tool ausgeliefert. Es ist keine Installation notwendig.

## One-Folder-Release

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

## Bedeutung der Ordner

- `MinAn.exe`: Startdatei
- `_internal`: reine Runtime- und Technikdateien
- `_internal/sample_data`: interner Bereich fuer die mitgelieferte Beispieldatei
- `output/reports`: Standardziel fuer HTML-Berichte
- `output/csv`: Standardziel fuer CSV-Exporte
- `README_Kurzstart.txt`: kompakte Einstiegshilfe direkt neben der EXE

## Build-Prozess

```batch
build_release.bat
```

Der Build bindet ein:

- `README_Kurzstart.txt`
- `_internal/sample_data/test_csv_deutsch_200x15.csv`

Die Output-Ordner werden beim Start oder bei erster Nutzung sichergestellt.

## Portabilitaet

- keine Nutzdaten in `_internal`
- keine stillen Benutzerverzeichnisse
- keine Abhaengigkeit von `tests\...` im Release
- alle relevanten Pfade relativ zum EXE-Ordner
