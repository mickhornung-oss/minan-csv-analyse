# Release Acceptance Checklist (v1.4.0)

Use this gate before declaring a local Windows release as accepted.

## A) Preconditions

- [ ] Python 3.10+ available in PATH
- [ ] dependencies installed via `pip install -r requirements.txt`
- [ ] repository state reviewed (no accidental artifact tracking)

## B) Quality Gate Execution

- [ ] run baseline gate: `python scripts/quality_gates.py`
- [ ] run full gate: `python scripts/quality_gates.py --with-build --with-exe-smoke`
- [ ] both commands exit with code `0`

## C) Build Output Integrity

- [ ] `dist/MinAn_1_4/MinAn.exe` exists
- [ ] `_internal/sample_data/test_csv_deutsch_200x15.csv` exists in release
- [ ] `output/reports` exists in release
- [ ] `output/csv` exists in release
- [ ] `README.md` exists in release root
- [ ] `README_Kurzstart.txt` exists in release root

## D) Runtime Smoke

- [ ] executable starts (`dist/MinAn_1_4/MinAn.exe`)
- [ ] app window renders
- [ ] bundled sample dataset can be loaded
- [ ] export targets resolve under release `output/`

## E) Repository and Documentation Consistency

- [ ] `README.md` reflects current release identity and scope
- [ ] `docs/packaging.md`, `docs/status.md`, `docs/release.md` match technical reality
- [ ] `CHANGELOG.md` contains the release entry
- [ ] `LICENSE` is present and explicit
- [ ] known limitations are documented without contradictions

## Acceptance Record (for maintainers)

- Release identity:
- Validation date:
- Validated by:
- Result: Accepted / Rejected
- Notes:
