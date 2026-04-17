# MinAn V1 - Umbau- und Abschlussplan (Blockplanung)

Stand: 2026-04-17
Strategie: grosser, produktiver Umbau in klaren Gruenzustaenden.

## Block 1 - Repo-Rahmen und Root-Hygiene

Ziel:
- Root auf Produktminimum reduzieren.
- Trennung zwischen Quellrepo und generierten Artefakten verbindlich machen.

Inhalte:
1. `.gitignore` auf reale Artefaktlage ausrichten (inkl. PyInstaller-Workdirs).
2. Artefaktpfade standardisieren (`build/`, `dist/`, `output/`) und fuer Repo-Sicht sauber regeln.
3. Leere/obsolete Root-Strukturen entfernen (z. B. leeres `sample_data/`).
4. Interne Arbeits-/Praesentationsinhalte klar als intern markieren oder aus Root-Buehne auslagern.

Gruenkriterium:
- `git status` zeigt keine ungeplanten Build-/Runtime-Artefakte.
- Root ist klar, knapp und produktorientiert.

## Block 2 - Doku-Architektur und Public-Einstieg

Ziel:
- Oeffentliche Doku konsistent und glaubwuerdig machen.

Inhalte:
1. `README.md` als zentrale Einstiegsschicht (Start, Nutzen, Build, Release in kompakter Form).
2. `docs/` in klare Schichten trennen: public user-facing vs. internal engineering.
3. Inkonsistenzen zwischen Release-Doku und realem Build-Verhalten beseitigen.
4. Kurzer "How to verify"-Pfad fuer externe Reviewer (Install -> Test -> Start).

Gruenkriterium:
- Ein externer Entwickler kann das Tool ohne Rueckfragen starten, testen und Build nachvollziehen.

## Block 3 - Packaging- und Release-Story haerten

Ziel:
- Release-Pfad als bewusstes Produktverfahren definieren.

Inhalte:
1. PyInstaller-Spec und Build-Skript auf konsistente Release-Inhalte trimmen.
2. Klar festlegen, welche Sample-Daten in den Release gehoeren.
3. Release-Artefakt-Checkliste einfuehren (Dateiinhalt, Struktur, Starttest, Smoke-Check).
4. Optional: reproduzierbare Versions-/Release-Notation vereinheitlichen.

Gruenkriterium:
- Build erzeugt reproduzierbar genau die dokumentierte Struktur.

## Block 4 - Codebase-Hardening ohne Architekturbruch

Ziel:
- Stabilitaet und Wartbarkeit erhoehen, ohne Komplettumbau.

Inhalte:
1. Logik-Duplikate zwischen Session-State und Transform-Service aufloesen.
2. Kritische Guardrails (Pfadschutz, Fehlerszenarien, Exportschutz) punktuell absichern.
3. Testluecken aus den Hardening-Anpassungen direkt schliessen.
4. Kleine Namens-/Schnittstellenkonsolidierungen mit hoher Wirkung.

Gruenkriterium:
- Tests bleiben gruen, Code wird klarer und entkoppelt.

## Block 5 - Public-Repo-Standardisierung

Ziel:
- Repository als serioeses oeffentliches Produktrepo abschliessen.

Inhalte:
1. `LICENSE` festziehen.
2. Basis-CI fuer Tests aufsetzen.
3. Optional: `CONTRIBUTING.md` + Issue/PR-Rahmen.
4. Minimalen Release-Nachweis fuer GitHub bereitstellen (Screenshot, Teststatus, Build-Info).

Gruenkriterium:
- Repo besteht den Erstcheck von externen Reviewern (Recruiter, Dev, OSS-Besucher).

## Block 6 - Finaler GitHub-/Release-Cut

Ziel:
- Endstand als bewusst kuratiertes Mini-Produkt veroeffentlichungsfaehig machen.

Inhalte:
1. Finalen Repo-Clean-Cut und Doku-Freeze durchfuehren.
2. End-to-end Verifikation: Start, Kernfunktionen, Export, Build, Tests.
3. Abschliessende Release-Readiness-Notiz mit expliziten Daten/Versionen.

Gruenkriterium:
- MinAn wirkt als kleines, fertiges, belastbares Desktop-Produkt mit professioneller Repo-Fuehrung.

## Umsetzungsreihenfolge (verbindlich)

1. Block 1
2. Block 2
3. Block 3
4. Block 4
5. Block 5
6. Block 6

Abweichungen nur bei nachweisbarer technischer Notwendigkeit.
