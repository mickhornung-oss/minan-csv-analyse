@echo off
setlocal
REM MinAn 1.4 - Release bauen (One-Folder via PyInstaller)

set RELEASE_VERSION=1_4
set RELEASE_DIR=%~dp0dist\MinAn_%RELEASE_VERSION%

echo === MinAn 1.4 - Release-Build ===

python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: PyInstaller nicht gefunden.
    echo Bitte installieren: pip install pyinstaller
    pause
    exit /b 1
)

python -m PyInstaller "%~dp0build\minan_v1.spec" --noconfirm
if errorlevel 1 (
    echo.
    echo Build fehlgeschlagen.
    pause
    exit /b 1
)

if not exist "%RELEASE_DIR%\_internal\sample_data" mkdir "%RELEASE_DIR%\_internal\sample_data"
if not exist "%RELEASE_DIR%\output\reports" mkdir "%RELEASE_DIR%\output\reports"
if not exist "%RELEASE_DIR%\output\csv" mkdir "%RELEASE_DIR%\output\csv"

copy /Y "%~dp0README_Kurzstart.txt" "%RELEASE_DIR%\README_Kurzstart.txt" >nul
copy /Y "%~dp0README.md" "%RELEASE_DIR%\README.md" >nul
copy /Y "%~dp0assets\sample_data\test_csv_deutsch_200x15.csv" "%RELEASE_DIR%\_internal\sample_data\test_csv_deutsch_200x15.csv" >nul

echo.
echo Build erfolgreich. Ausgabe in: dist\MinAn_%RELEASE_VERSION%\
echo Erwartete Struktur:
echo   MinAn.exe
echo   _internal\sample_data\
echo   output\reports\
echo   output\csv\
echo   README_Kurzstart.txt
echo   README.md
pause
