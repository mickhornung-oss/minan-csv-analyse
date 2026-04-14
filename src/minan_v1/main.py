"""Startpunkt der MinAn 1.4 Desktop-Anwendung."""

import sys
from pathlib import Path

# Sicherstellen, dass src/ im Importpfad liegt
_src_dir = str(Path(__file__).resolve().parent.parent)
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from minan_v1.app import run_app


def main() -> None:
    """Haupteinstiegspunkt."""
    sys.exit(run_app())


if __name__ == "__main__":
    main()
