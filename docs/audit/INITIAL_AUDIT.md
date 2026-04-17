# MinAn V1 - Initial Audit (Senior-Diagnose)

Stand: 2026-04-17
Scope: Vollaufnahme des kompletten Projektordners inkl. Start-, Build-, Test-, Doku- und Release-Kanten.

## 1) Harte Ist-Einschaetzung

MinAn ist technisch kein Bastelcode, sondern ein funktionierender, testbarer Desktop-Kern mit realer Produktsubstanz.
Gleichzeitig ist das Repository in seiner aktuellen Form nicht sauber kuratiert fuer eine oeffentliche Produktwirkung.
Die Hauptschwaeche liegt nicht im Kerncode, sondern in Repo-Hygiene, Trennschaerfe zwischen Produkt und Artefakten sowie fehlenden Public-Standards.

Kurzform:
- Produktkern: solide
- Testbasis: solide
- Release-Naehe: vorhanden
- Public-Repo-Aussenwirkung: derzeit mittelmaessig bis unruhig

## 2) Bewertungsdimensionen

### Strukturqualitaet
- Positiv: `src/minan_v1` ist in Domain/Services/UI/Utils getrennt.
- Negativ: Root enthaelt viele nicht-kernige Bereiche ohne klare interne/oeffentliche Trennpolitik.

### Wartbarkeit
- Positiv: Session-State + Service-Schicht klar erkennbar.
- Positiv: Testset deckt Kernablaeufe inkl. GUI-Smoke ab.
- Negativ: Teilweise Code-Duplizierung von Filter-/Outlier-Logik zwischen `SessionState` und `transform_service`.

### Start-/Nutzbarkeit
- Positiv: `run_dev.bat` und `build_release.bat` sind niedrigschwellig.
- Positiv: Quickstart-Dialog und Beispiel-Datei-Fluss vorhanden.
- Negativ: Repo macht den Unterschied zwischen Entwickler-Workspace und distributable Produkt noch nicht konsequent sichtbar.

### Build-/Packaging-Reife
- Positiv: PyInstaller-Story vorhanden (`build/minan_v1.spec`, `windows_version_info.txt`).
- Negativ: `build/` ist als Arbeits-/Artefaktordner im laufenden Zustand unaufgeraeumt.
- Negativ: Release-Doku und realer Dist-Inhalt sind nicht voll deckungsgleich (Doku spricht von einem Sample, Dist enthaelt mehrere Sample-CSV).

### Public-Repo-Glaubwuerdigkeit
- Positiv: README + Doku + Tests existieren.
- Negativ: Fehlende Standard-Repodateien (mindestens `LICENSE`; sinnvoll: CI, CONTRIBUTING-Rahmen).
- Negativ: Interne Praesentation und Produktrepo sind nicht stark genug entkoppelt.

## 3) Harte Problemliste (priorisiert)

1. Repo-Hygiene unzureichend
- Build-/Arbeitsartefakte liegen im Projektbaum (`build/work`, TOC/PKG etc.).
- `git status` zeigt `build/` als untracked Bereich.

2. Dominanz von Artefakten gegenueber Kernstruktur
- `dist/` und `build/` sind groessenmaessig deutlich groesser als der eigentliche Code.
- Das schwaecht die Wahrnehmung als bewusst gefuehrtes Produktrepo.

3. Unklare Trennung zwischen Produkt-, interner und praesentationsbezogener Ebene
- `presentation/` + `scripts/presentation/` sind intern sinnvoll, aber im Hauptbild des Repos zu dominant.

4. Doku/Packaging-Inkonsistenz
- Release-Beschreibung fokussiert schlanke Sample-Struktur, reale Dist-Inhalte enthalten jedoch mehrere Sample-CSV durch Spec-Datas.

5. Fehlende Public-Standardisierung
- Kein `LICENSE` im Root.
- Keine CI-Pipeline dokumentiert/abgelegt.
- Kein klarer Beitragspfad fuer externe Mitwirkende.

6. Kleine Strukturaltlasten
- Leerer Root-Ordner `sample_data/`.
- Mehrere interne Ergebnisdateien in `output/`.

## 4) Rettungsentscheidung

## Entscheidung: B

Variante B: Bestehendes Projekt ist nur teilweise sauber und braucht einen starken strukturellen Umbau.

Begruendung:
- Gegen Variante C (Neuaufsetzen): Der Kern ist technisch tragfaehig, Tests sind gruen, Desktop-Fluss funktioniert. Ein Neuaufsetzen waere Overkill und wuerde Zeit ohne Mehrwert verbrennen.
- Gegen Variante A (nur Politur): Die Repo- und Artefaktlage ist zu unruhig fuer Public-Product-Anspruch. Reine Kosmetik reicht nicht.

Fazit:
- Codebasis retten und behalten.
- Repo-Struktur, Artefakt-Strategie, Doku-Architektur und Release-Story konsequent neu ordnen.

## 5) Zielbild (fachlich verbindlich)

MinAn soll als kleines, lokales Desktop-Mini-Produkt wirken, nicht als Arbeitsablage.

Zielzustand:
- Root ist knapp und produktorientiert.
- Produktkern (`src`), Tests (`tests`), kuratierte Doku (`docs`) sind klar getrennt.
- Build-/Dist-/Output-Artefakte sind aus dem Repo-Hauptbild entfernt oder strikt in interne Pfade ausgelagert.
- Packaging-Story ist eindeutig: wie bauen, was entsteht, was wird veroeffentlicht, was bleibt intern.
- Public-Repo-Standards sind vorhanden (Lizenz, CI-Grundlauf, klare Einstiegspfade).

Soll-Wirkung fuer GitHub-Besucher:
- Sofort verstehbar, was das Produkt tut.
- Sofort reproduzierbar, wie man startet/testet/baut.
- Keine Altlast-Atmosphaere, keine technische Unruhe auf Root-Ebene.

## 6) Desktop-/Mini-Programm-Reife (Ist vs. Soll)

Ist-Staerken:
- GUI mit klaren Tabs und durchgaengigem CSV->Analyse->Export-Fluss.
- Portable Pfadlogik vorhanden.
- EXE-Build vorhanden.

Ist-Luecken:
- Arbeitsartefakte und Begleitmaterial schwaechen den "fertiges Mini-Programm"-Eindruck im Repo.
- Release-Story ist technisch da, aber repo-strategisch noch nicht sauber geschnitten.

Soll:
- Repo zeigt vorrangig Produkt, nicht Werkbank.
- Release-Nachweise sind gezielt und knapp, nicht durch Massendateien.

## 7) Nicht-Ziele dieses Blocks (erfuellt)

- Kein grosses Refactoring am Codekern.
- Keine vorschnellen strukturellen Loeschungen.
- Keine kosmetische Umbau-Show ohne Diagnose.

Dieses Dokument ist Diagnose- und Entscheidungsgrundlage fuer den naechsten Umsetzungsblock.
