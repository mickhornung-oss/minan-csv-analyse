@echo off
REM MinAn 1.4 - Entwicklungsmodus starten

echo === MinAn 1.4 - Dev-Start ===

python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python wurde nicht gefunden.
    echo Bitte Python 3.10+ installieren und zum PATH hinzufuegen.
    pause
    exit /b 1
)

python "%~dp0src\minan_v1\main.py"
if errorlevel 1 (
    echo.
    echo Anwendung wurde mit Fehler beendet.
    pause
)
