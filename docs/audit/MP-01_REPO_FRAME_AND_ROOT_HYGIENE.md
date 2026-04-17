# MP-01 - Repo-Rahmen und Root-Hygiene

Stand: 2026-04-17
Block: 1/5
Status: abgeschlossen

## Ziel dieses Blocks

- Root auf produktrelevante Einstiegselemente reduzieren.
- Build-/Dist-/Output-Artefakte aus der Hauptbuehne entfernen.
- `.gitignore` an die reale Arbeitsweise anpassen.
- Public-relevante und interne Inhalte klarer trennen.

## Durchgefuehrte Strukturentscheidungen

### 1) Root-Rahmen bereinigt

Behandelte Root-Elemente:

KEEP IN ROOT:
- `src/`, `tests/`, `assets/`, `docs/`, `scripts/`, `packaging/`
- `README.md`, `README_Kurzstart.txt`, `requirements.txt`, `run_dev.bat`, `build_release.bat`, `.gitignore`

MOVE TO INTERNAL:
- `presentation/*` -> `docs/internal/presentation/*`
- `scripts/presentation/*` -> `docs/internal/presentation/scripts/*`

REMOVE FROM WORKTREE (generiert):
- `build/` (komplett entfernt)
- `dist/` (komplett entfernt)
- `output/` (komplett entfernt)
- leeres Root-`sample_data/` (entfernt)

### 2) Packaging-Quellen von Build-Artefakten getrennt

Verschoben:
- `build/minan_v1.spec` -> `packaging/pyinstaller/minan_v1.spec`
- `build/windows_version_info.txt` -> `packaging/pyinstaller/windows_version_info.txt`

Angepasst:
- `build_release.bat` nutzt jetzt `packaging/pyinstaller/minan_v1.spec`.
- Spec-Pfade wurden auf neuen Speicherort korrigiert.

Ergebnis:
- Versionierte Build-Konfiguration ist vom generierten `build/`-Muell entkoppelt.

### 3) Artefaktpolitik verhaertet (`.gitignore`)

Neu geregelt:
- `build/` und `dist/` komplett ignoriert.
- `output/` komplett ignoriert.
- Python-/Test-/Tool-Caches konsolidiert (`__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, Coverage-Outputs).
- Editor-/OS-Rauschen und lokale Agent-Konfiguration (`.claude/`) ignoriert.

Ergebnis:
- Lokale Build- und Laufartefakte dominieren den Git-Status nicht mehr.

### 4) Public vs. intern klarer getrennt

Neu eingefuehrt:
- `docs/internal/README.md` als Einordnung fuer interne Inhalte.
- `packaging/README.md` als Einordnung fuer versionierte Packaging-Quellen.

Aktualisiert:
- `README.md` Verweis auf interne Praesentationsskripte.
- `scripts/README.md` Verweise auf neuen internen Pfad.
- `docs/internal/presentation/scripts/README.md` Zielpfad aktualisiert.
- interne Praesentationsskripte auf neuen Speicherort umgestellt.

## Validierung

- Root wirkt nach Entfernen von `build/`, `dist/`, `output/`, `sample_data/` deutlich ruhiger.
- Interne Praesentationsmaterialien liegen nicht mehr auf der Root-Hauptbuehne.
- Packaging-Konfiguration bleibt versioniert und ausfuehrbar im Repo.
- Ignore-Regeln passen zu realen generierten Datenarten.

## Bewusst nicht angefasst (Scope-Grenze)

- Kein Fachlogik-Refactoring in `src/`.
- Keine README-Endinszenierung.
- Kein Packaging-Feintuning ueber Pfadkonsolidierung hinaus.
- Keine CI-Einfuehrung.

## Offene Folgearbeiten (fuer naechste Bloecke)

- Doku-Architektur und Public-Einstiegsfluss konsolidieren (Block 2).
- Release-/Packaging-Story im Detail schliessen (Block 3).
