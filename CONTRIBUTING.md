# Contributing

## Contribution Scope

MinAn is currently maintained as a focused desktop mini-product.
Contributions should prioritize stability, clarity, and reproducibility.

## Before Opening a PR

1. Sync to latest `main`.
2. Run:
   - `pip install -r requirements.txt`
   - `pytest -q`
3. Keep changes scoped to one concern (bugfix, docs, packaging, or small refactor).
4. Do not commit generated artifacts from `build/`, `dist/`, or `output/`.

## Pull Request Expectations

- Clear problem statement
- Minimal, reviewable diff
- Updated docs/tests where behavior changes
- No unrelated formatting churn

## Non-goals for PRs

- Feature expansion without prior alignment
- Large unscoped refactors
- Breaking the local-first desktop model
