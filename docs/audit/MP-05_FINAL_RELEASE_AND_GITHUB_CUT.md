# MP-05 - Final Release and GitHub Cut

Date: 2026-04-17  
Block objective: final release identity, governance closure, and public repository finish.

## 1) Initial gaps before MP-05

- No explicit public release identity documented as a final cut.
- No formal changelog file.
- License state was unresolved in public docs.
- Release checklist existed but was operational and not yet framed as a formal acceptance gate.
- Public release-note document for final baseline was missing.

## 2) Final decisions and implementation

### A) Release identity fixed

- Final release identity set to `v1.4.0`.
- Kept consistent with existing packaging output naming (`dist/MinAn_1_4/`).
- Reflected in `README.md`, `docs/status.md`, `docs/packaging.md`, `docs/release.md`, and `CHANGELOG.md`.

### B) Changelog and release notes finalized

- Added root `CHANGELOG.md` with factual entries for the consolidated product baseline.
- Added `docs/release.md` as formal release notes for `v1.4.0` (scope, included/not included, output, validation path).

### C) License state resolved

- Added root `LICENSE` with explicit "All Rights Reserved" terms.
- Public repo state is now legally explicit (source-available, no open-source grant).

### D) Release acceptance gate formalized

- Reworked `docs/release_checklist.md` into a formal release acceptance checklist.
- Gate now covers:
  - prerequisites
  - baseline + full quality-gate execution
  - build output integrity
  - runtime smoke checks
  - repo/docs/governance consistency
  - acceptance record fields

### E) Public docs consistency pass

- Updated `README.md` to include release identity, release/changelog references, and explicit license section.
- Updated `docs/README.md` to include `docs/release.md`.
- Updated `docs/status.md` to remove outdated statement about missing CI and reflect actual CI baseline.
- Updated `docs/packaging.md` with release identity and consistency with formal release gate references.

## 3) Final release structure definition (unchanged technically, now formalized)

Release output remains:

- `dist/MinAn_1_4/MinAn.exe`
- `dist/MinAn_1_4/_internal/sample_data/test_csv_deutsch_200x15.csv`
- `dist/MinAn_1_4/output/reports/`
- `dist/MinAn_1_4/output/csv/`
- `dist/MinAn_1_4/README.md`
- `dist/MinAn_1_4/README_Kurzstart.txt`

## 4) Validation executed in MP-05

Target validation commands:

- `python scripts/quality_gates.py`
- `python scripts/quality_gates.py --with-build --with-exe-smoke`

Result: executed and green.
- `python scripts/quality_gates.py` -> pass (`155 passed`)
- `python scripts/quality_gates.py --with-build --with-exe-smoke` -> pass (build success, EXE smoke success)

## 5) Remaining minimal open points

- No automated GitHub release artifact publishing workflow (deliberately out of scope).
- No cross-platform packaging expansion (Windows-only by design).

## 6) MP-05 outcome

MP-05 closes release/governance/public-finish requirements for a publishable `v1.4.0` repository baseline.
The project is in an academically and portfolio-credible final cut state.
