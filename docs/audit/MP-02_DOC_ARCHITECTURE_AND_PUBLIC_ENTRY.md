# MP-02 - Documentation Architecture and Public Entry Consolidation

Date: 2026-04-17
Block: 2/5
Status: completed

## Objective

Create a clear public documentation surface for external users/reviewers while preserving internal historical material.

## Key Decisions

1. Public docs are English-first.
2. `README.md` is the single public entry door.
3. `docs/README.md` is the public docs index.
4. Internal and historical docs are explicitly separated under `docs/internal/`.
5. Documentation statements were aligned with real project behavior and current repository structure.

## Implemented Changes

### A) README rebuilt as public entry point

`README.md` was rewritten with a strict public-repo structure:

- product overview
- status/scope/demo truth statement
- core features
- tech stack
- quickstart (dev + portable build)
- testing/quality gates
- packaging/build source of truth
- docs navigation
- repository structure
- known limitations

Notable truth constraints documented:

- no hosted public demo
- local Windows-first workflow
- no finalized public license file yet
- no CI pipeline documented yet

### B) Public docs architecture introduced

Added a clear docs index and focused public guides:

- `docs/README.md`
- `docs/architecture.md` (rewritten in English)
- `docs/usage.md`
- `docs/development.md`
- `docs/testing.md`
- `docs/packaging.md`
- `docs/status.md`

### C) Internal/public separation hardened

Archived previous German public docs into internal legacy location:

- `docs/internal/legacy-de/analysis_scope.de.md`
- `docs/internal/legacy-de/dataflow.de.md`
- `docs/internal/legacy-de/release.de.md`
- `docs/internal/legacy-de/release_status.de.md`
- `docs/internal/legacy-de/testplan.de.md`
- `docs/internal/legacy-de/user_guide.de.md`

Added internal meta docs:

- `docs/internal/README.md`
- `docs/internal/legacy-de/README.md`

Result: public docs are no longer mixed with historical German narrative in root `docs/`.

### D) Contributor-facing repo standard

Added:

- `CONTRIBUTING.md`

Purpose:

- basic PR quality expectations
- scope boundaries
- artifact policy reminder

## Documentation Truth Checks

Validated against repository behavior:

- Start path: `run_dev.bat` and `python src/minan_v1/main.py`
- Test command: `pytest -q`
- Packaging entry: `build_release.bat`
- Packaging source files: `packaging/pyinstaller/*`
- Generated artifact policy: `build/`, `dist/`, `output/` excluded from git
- Sample data statement adjusted to avoid overclaiming exact packaged file count

## Non-goals kept intact

- no feature work
- no core code refactor
- no CI rollout
- no release-system deep changes

## Result

Public onboarding quality is materially improved:

- faster external comprehension
- reduced doc ambiguity
- clearer public/internal boundary
- traceable, reproducible entry path for reviewers
