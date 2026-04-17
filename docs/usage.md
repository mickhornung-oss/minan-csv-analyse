# Usage Guide

## Who This Is For

Users who want to inspect CSV files locally on Windows without cloud dependencies.

## Start Modes

### Developer mode

- `run_dev.bat`

### Portable release mode

- `dist\\MinAn_1_4\\MinAn.exe`

## Typical Workflow

1. Click **CSV oeffnen** and select a CSV file.
2. Review overview, metrics, charts, and table tabs.
3. Optionally refine the active view in **Bearbeiten**.
4. Export active view:
   - CSV via **Export** tab
   - HTML report via toolbar or **Export** tab

## Sample Dataset

A sample CSV is bundled in `assets/sample_data/` and copied into release runtime sample path during build.

## Output Locations

Default output folders:

- `output/reports` for HTML reports
- `output/csv` for CSV exports

## Safety Guarantees

- Source file is not modified by MinAn
- Export/report writes to new target files
- Attempting to overwrite source file is rejected
