@echo off
setlocal
REM MinAn 1.4 - Release bauen (One-Folder via PyInstaller)

set PROJECT_ROOT=%~dp0
set RELEASE_VERSION=1_4
set RELEASE_DIR=%PROJECT_ROOT%dist\MinAn_%RELEASE_VERSION%
set BUILD_DIR=%PROJECT_ROOT%build
set SPEC_FILE=%PROJECT_ROOT%packaging\pyinstaller\minan_v1.spec
set VERSION_FILE=%PROJECT_ROOT%packaging\pyinstaller\windows_version_info.txt
set SAMPLE_FILE=%PROJECT_ROOT%assets\sample_data\test_csv_deutsch_200x15.csv
set EXE_PATH=%RELEASE_DIR%\MinAn.exe

echo === MinAn 1.4 - Release-Build ===

python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: PyInstaller nicht gefunden.
    echo Bitte installieren: pip install pyinstaller
    exit /b 1
)

if not exist "%SPEC_FILE%" (
    echo FEHLER: Spec-Datei fehlt: %SPEC_FILE%
    exit /b 1
)
if not exist "%VERSION_FILE%" (
    echo FEHLER: Version-Datei fehlt: %VERSION_FILE%
    exit /b 1
)
if not exist "%SAMPLE_FILE%" (
    echo FEHLER: Beispiel-CSV fehlt: %SAMPLE_FILE%
    exit /b 1
)

if exist "%BUILD_DIR%" rmdir /S /Q "%BUILD_DIR%"
if exist "%RELEASE_DIR%" rmdir /S /Q "%RELEASE_DIR%"

python -m PyInstaller "%SPEC_FILE%" --noconfirm --clean
if errorlevel 1 (
    echo.
    echo Build fehlgeschlagen.
    exit /b 1
)

if not exist "%EXE_PATH%" (
    echo FEHLER: Build abgeschlossen, aber MinAn.exe fehlt: %EXE_PATH%
    exit /b 1
)

if not exist "%RELEASE_DIR%\_internal\sample_data" mkdir "%RELEASE_DIR%\_internal\sample_data"
if not exist "%RELEASE_DIR%\output\reports" mkdir "%RELEASE_DIR%\output\reports"
if not exist "%RELEASE_DIR%\output\csv" mkdir "%RELEASE_DIR%\output\csv"

copy /Y "%~dp0README_Kurzstart.txt" "%RELEASE_DIR%\README_Kurzstart.txt" >nul
copy /Y "%~dp0README.md" "%RELEASE_DIR%\README.md" >nul

echo.
echo Build erfolgreich. Ausgabe in: dist\MinAn_%RELEASE_VERSION%\
echo Erwartete Struktur:
echo   MinAn.exe
echo   _internal\sample_data\
echo   output\reports\
echo   output\csv\
echo   README_Kurzstart.txt
echo   README.md
exit /b 0
