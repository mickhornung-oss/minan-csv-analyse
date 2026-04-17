#!/usr/bin/env python3
"""Exportiert die aktuelle Praesentation nach PDF via PowerPoint COM."""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[4]
pptx_path = project_root / "docs" / "internal" / "presentation" / "MinAn_1_4_Abschlusspraesentation.pptx"
pdf_path = project_root / "docs" / "internal" / "presentation" / "MinAn_1_4_Abschlusspraesentation.pdf"

if not pptx_path.exists():
    print(f"[ERROR] {pptx_path} nicht gefunden")
    sys.exit(1)

try:
    import win32com.client as win32
except ImportError:
    print("[SKIP] pywin32 nicht installiert (pip install pywin32)")
    sys.exit(0)

try:
    ppt = win32.Dispatch("PowerPoint.Application")
    ppt.Visible = False
    presentation = ppt.Presentations.Open(str(pptx_path.resolve()))
    presentation.ExportAsFixedFormat(str(pdf_path.resolve()), 2, 1)
    presentation.Close()
    ppt.Quit()
    print(f"[OK] PDF exportiert: {pdf_path}")
except Exception as exc:
    print(f"[ERROR] PowerPoint-Export fehlgeschlagen: {exc}")
    sys.exit(1)

