"""App-Initialisierung fuer MinAn 1.4."""

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from minan_v1.config import APP_PRODUCT_NAME, APP_TITLE, WINDOW_MIN_HEIGHT, WINDOW_MIN_WIDTH
from minan_v1.domain.session_state import SessionState
from minan_v1.resources import ensure_runtime_dirs, icon_path
from minan_v1.ui.main_window import MainWindow


def run_app() -> int:
    """Initialisiert und startet die Desktop-Anwendung."""
    app = QApplication([])
    app.setApplicationName(APP_PRODUCT_NAME)
    ensure_runtime_dirs()
    app_icon = icon_path("minan_v1.ico")
    if app_icon.exists():
        app.setWindowIcon(QIcon(str(app_icon)))

    session = SessionState()

    window = MainWindow(session)
    window.setWindowTitle(APP_TITLE)
    window.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    window.show()

    return app.exec()
