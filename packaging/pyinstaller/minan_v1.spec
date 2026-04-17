# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller Spec-Datei fuer MinAn 1.4 - One-Folder-Release."""

from pathlib import Path

block_cipher = None

PROJECT_ROOT = Path(SPECPATH).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
ASSETS_DIR = PROJECT_ROOT / "assets"
ICON_PATH = ASSETS_DIR / "icons" / "minan_v1.ico"
SAMPLE_FILE_NAME = "test_csv_deutsch_200x15.csv"
SAMPLE_FILE_PATH = ASSETS_DIR / "sample_data" / SAMPLE_FILE_NAME
VERSION_INFO_PATH = Path(SPECPATH) / "windows_version_info.txt"
APP_VERSION = "1.4"
DIST_NAME = f"MinAn_{APP_VERSION.replace('.', '_')}"

if not ICON_PATH.exists():
    raise FileNotFoundError(f"Icon file missing: {ICON_PATH}")
if not SAMPLE_FILE_PATH.exists():
    raise FileNotFoundError(f"Sample CSV missing: {SAMPLE_FILE_PATH}")
if not VERSION_INFO_PATH.exists():
    raise FileNotFoundError(f"Version info file missing: {VERSION_INFO_PATH}")

datas = [
    (str(ICON_PATH), "assets/icons"),
    (str(SAMPLE_FILE_PATH), "sample_data"),
]

a = Analysis(
    [str(SRC_DIR / "minan_v1" / "main.py")],
    pathex=[str(SRC_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "minan_v1",
        "minan_v1.app",
        "minan_v1.config",
        "minan_v1.domain",
        "minan_v1.services",
        "minan_v1.ui",
        "minan_v1.utils",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MinAn",
    icon=str(ICON_PATH),
    version=str(VERSION_INFO_PATH),
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=DIST_NAME,
)
