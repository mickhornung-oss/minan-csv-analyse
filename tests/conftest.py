"""Pytest-Konfiguration und gemeinsame Fixtures fuer MinAn 1.4."""

import os
import sys
from pathlib import Path

import pandas as pd
import pytest
from PySide6.QtWidgets import QApplication

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# src/ zum Importpfad hinzufuegen
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


@pytest.fixture(scope="session")
def qapp():
    """Offscreen-QApplication fuer UI-Tests."""
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture(autouse=True)
def close_matplotlib_figures():
    """Schliesst alle offenen matplotlib-Figures nach jedem Test.

    Verhindert die Warnung "More than 20 figures have been opened"
    indem Figures nach jedem Test freigegeben werden.
    """
    yield
    import matplotlib.pyplot as plt
    plt.close('all')


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Einfacher Test-DataFrame mit gemischten Typen und Fehlwerten."""
    return pd.DataFrame({
        "ID": [1, 2, 3, 4, 5],
        "Name": ["Alice", "Bob", "Charlie", None, "Eve"],
        "Alter": [30, 25, 35, 28, 42],
        "Stadt": ["Berlin", "Muenchen", "Berlin", "Hamburg", "Berlin"],
        "Gehalt": [50000.0, 45000.0, 60000.0, None, 55000.0],
        "Aktiv": [True, True, False, True, True],
    })


@pytest.fixture
def df_with_duplicates() -> pd.DataFrame:
    """DataFrame mit doppelten Zeilen."""
    return pd.DataFrame({
        "A": [1, 2, 3, 1, 2],
        "B": ["x", "y", "z", "x", "y"],
    })


@pytest.fixture
def df_with_problems() -> pd.DataFrame:
    """DataFrame mit diversen Qualitaetsproblemen."""
    return pd.DataFrame({
        "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Leer": [None, None, None, None, None, None, None, None, None, None],
        "Konstant": ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
        "VieleFehler": [1, None, None, None, None, None, None, None, 9, 10],
        "Normal": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    })


@pytest.fixture
def df_with_outliers() -> pd.DataFrame:
    """DataFrame mit klaren Ausreisser-Kandidaten."""
    return pd.DataFrame({
        "ID": list(range(1, 9)),
        "Wert": [10, 11, 12, 13, 14, 15, 16, 200],
        "Kategorie": ["A", "A", "A", "B", "B", "B", "B", "B"],
    })


@pytest.fixture
def tmp_csv(tmp_path, sample_df) -> Path:
    """Erstellt eine temporaere CSV-Datei zum Testen."""
    csv_path = tmp_path / "test_data.csv"
    sample_df.to_csv(csv_path, index=False, encoding="utf-8")
    return csv_path


@pytest.fixture
def tmp_csv_semicolon(tmp_path) -> Path:
    """CSV mit Semikolon-Separator."""
    csv_path = tmp_path / "test_semi.csv"
    df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    df.to_csv(csv_path, index=False, sep=";", encoding="utf-8")
    return csv_path


@pytest.fixture
def tmp_csv_latin1(tmp_path) -> Path:
    """CSV mit Latin-1 Encoding und Umlauten."""
    csv_path = tmp_path / "test_latin1.csv"
    content = "Name,Stadt\nM\u00fcller,M\u00fcnchen\nSchr\u00f6der,K\u00f6ln\n"
    csv_path.write_bytes(content.encode("latin-1"))
    return csv_path


@pytest.fixture
def sample_data_dir() -> Path:
    """Pfad zum assets/sample_data Verzeichnis."""
    return Path(__file__).resolve().parent.parent / "assets" / "sample_data"
