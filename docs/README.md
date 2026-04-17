# Documentation Index

This directory is split into **public product/developer documentation** and **internal project documentation**.

## Public Documentation

- [`architecture.md`](architecture.md): technical architecture and data-flow model
- [`usage.md`](usage.md): user-facing local usage flow
- [`development.md`](development.md): developer setup and run instructions
- [`testing.md`](testing.md): test execution and quality checks
- [`packaging.md`](packaging.md): release packaging and artifact policy
- [`release.md`](release.md): release identity, scope, and included artifacts
- [`release_checklist.md`](release_checklist.md): formal release acceptance gate
- [`status.md`](status.md): current project status and scope boundaries

## Internal Documentation

- [`audit/`](audit/): technical audit and block-level transformation records
- [`internal/`](internal/): internal-only supporting material (presentation assets, legacy docs)

## Navigation Rule

If you are new to the project:

1. Read `../README.md`
2. Read `development.md`
3. Run `python scripts/quality_gates.py`
4. Build with `build_release.bat` if packaging validation is needed
