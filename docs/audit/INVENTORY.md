# MinAn V1 - Projektinventar (Initialblock)

Stand: 2026-04-17
Pfad: `C:\Users\mickh\Desktop\Mini Analyse Tool\MinAn V1`

## 1) Gesamtstruktur (Ist)

Top-Level-Verzeichnisse:
- `.claude/`
- `.git/`
- `.pytest_cache/`
- `assets/`
- `build/`
- `dist/`
- `docs/`
- `output/`
- `presentation/`
- `sample_data/` (leer)
- `scripts/`
- `src/`
- `tests/`

Top-Level-Dateien:
- `.gitignore`
- `README.md`
- `README_Kurzstart.txt`
- `requirements.txt`
- `run_dev.bat`
- `build_release.bat`

## 2) Mengen-/Groessenbild (Dateien)

Ermittelte Dateigroessen nach Top-Level-Bereich:
- `dist/`: 1095 Dateien, ~193.88 MB
- `build/`: 34 Dateien, ~68.10 MB
- `presentation/`: 29 Dateien, ~2.54 MB
- `assets/`: 6 Dateien, ~0.84 MB
- `output/`: 5 Dateien, ~0.44 MB
- `tests/`: 51 Dateien, ~0.38 MB
- `src/`: 70 Dateien, ~0.31 MB
- `docs/`: 8 Dateien, ~0.03 MB
- `scripts/`: 14 Dateien, ~0.08 MB

Interpretation:
- Das Repository ist aktuell stark artefaktlastig.
- Der produktive Quellcode ist vergleichsweise klein; Build-/Release-Artefakte dominieren die physische Struktur.

## 3) Kategorisierte Bestandsaufnahme

### A. Produktivkern (hoch relevant)

- `src/minan_v1/`
  - `main.py`, `app.py`, `config.py`, `resources.py`
  - `domain/` (Modelle, Enums, Session-State)
  - `services/` (Import, Profiling, Quality, Charts, Export, Report, Transform)
  - `ui/` (MainWindow, Dialoge, Widgets, Table-Model)
  - `utils/`

Bewertung: produktiv relevant, klar als App-Kern erkennbar.

### B. Tests (hoch relevant)

- `tests/` mit 15+ Testmodulen
- Schwerpunkte: Import, Profiling, Quality, Transform, Export, Report, Runtime-Pfade, GUI-Smoke
- Lauf: `pytest -q` erfolgreich mit `155 passed in 6.84s`

Bewertung: für kleines Desktop-Tool überdurchschnittlich solide Testabdeckung im Kernpfad.

### C. Nutzer-/Produktdoku (relevant)

- Root: `README.md`, `README_Kurzstart.txt`
- `docs/`: `architecture.md`, `dataflow.md`, `analysis_scope.md`, `testplan.md`, `user_guide.md`, `release.md`, `RELEASE_STATUS.md`

Bewertung: umfangreiche Doku vorhanden; Fokus liegt auf Produktfunktion und Release-Nutzung.

### D. Build-/Packaging-Dateien (relevant, aber unaufgeraeumt)

- `build_release.bat`
- `build/minan_v1.spec`
- `build/windows_version_info.txt`

Bewertung: prinzipiell vorhanden, aber `build/` enthaelt zusaetzlich große temporäre PyInstaller-Artefakte (`work`, TOC, PKG, EXE-Zwischenstaende).

### E. Release-Artefakte (nicht ins Standard-Repo)

- `dist/MinAn_1_4/` inkl. EXE und `_internal`

Bewertung: als lokales Release okay, im Projektarbeitsbaum als Dauerelement fuer Public-Repo unruhig.

### F. Betriebs-/Laufzeitdaten (nicht in Kernrepo)

- `output/reports/*.html`
- `output/csv/*.csv`

Bewertung: lokal sinnvoll, im Entwicklungsrepo als persistente Inhalte nur begrenzt sinnvoll.

### G. Interne Begleit-/Praesentationsartefakte (niedrig relevant)

- `presentation/*.pptx`, `presentation/*.pdf`, `presentation/generated_assets/*`
- `scripts/presentation/*`

Bewertung: fachlich nachvollziehbar als Projektbegleitung, aber fuer ein klares Produktrepo randstaendig.

### H. Historisch/technisch auffaellige Punkte

- Leerer Ordner `sample_data/` im Root.
- `build/` aktuell unversioniert und als untracked Zustand sichtbar (`git status` zeigt `?? build/`).
- `dist/` existiert lokal mit sehr großem Umfang.
- Cache-Verzeichnisse lokal vorhanden (`.pytest_cache`, `__pycache__`), durch Ignore weitgehend abgefangen.

## 4) Produktiv vs. Altlast - harte Trennung

Produktiv relevant:
- `src/`, `tests/`, `assets/icons`, `assets/sample_data`, `README.md`, `README_Kurzstart.txt`, `requirements.txt`, `run_dev.bat`, `build_release.bat`, ausgewählte `docs/`.

Strukturell/oeffentlich problematisch oder nur intern:
- `build/work`, `build/minan_v1/*` Build-Zwischenartefakte
- `dist/*` gebaute Release-Binaries im Arbeitsbaum
- `output/*` erzeugte Reports/CSV
- `presentation/*` inkl. generated assets
- leerer Root-Ordner `sample_data/`

## 5) Repo-Tauglichkeit (Inventar-Sicht)

Positiv:
- Klarer Python-Desktop-Kern.
- Reproduzierbarer Testlauf.
- Explizite Start-/Build-Skripte.
- Domain/Service/UI-Struktur vorhanden.

Negativ:
- Root wirkt historisch gewachsen statt kuratiert.
- Artefakt- und Begleitmaterial-Anteil im selben Arbeitsbaum ist hoch.
- Fehlende typische Public-Repo-Standards (z. B. `LICENSE`, CI-Workflow, klarer Contributing-/Issue-Rahmen).
