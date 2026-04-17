# Architecture

## Layered Design

MinAn follows a pragmatic layered design:

- `ui/`: desktop presentation layer (PySide6)
- `services/`: business/application logic
- `domain/`: session and model definitions
- `utils/`: supporting helpers without business ownership

Dependency direction:

```text
UI -> Services -> Domain
UI -> Utils
Services -> Utils
```

Services do not depend on UI widgets.

## Core Runtime Model

`SessionState` is the runtime center:

- keeps `original_df` (source snapshot)
- keeps `working_df` (editable copy)
- builds `current_df` (active filtered/quick-view state)
- stores profile, quality report, summary, and last export/report metadata

## Data Safety Model

- Source CSV is read-only from workflow perspective
- All edits are applied to working copy
- Exports generate new files
- Overwriting source file is blocked by export/report services

## Main Modules

- `services/import_service.py`: CSV loading and detection
- `services/profile_service.py`: structural profiling
- `services/quality_service.py`: quality findings
- `services/transform_service.py`: edit/filter helpers
- `services/export_service.py`: CSV export
- `services/report_service.py`: HTML reporting
- `ui/main_window.py`: main interaction shell

## Runtime Paths

Path behavior is centralized in `src/minan_v1/resources.py` and `src/minan_v1/config.py`.

- Dev mode: project-root relative paths
- Frozen mode: executable-root relative paths
- Runtime folders are ensured before operations (`output/reports`, `output/csv`)
