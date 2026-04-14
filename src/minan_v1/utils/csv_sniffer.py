"""CSV-Sniffer: Automatische Erkennung von Separator und Encoding."""

import csv
import io
from pathlib import Path

from minan_v1.config import CSV_SNIFF_BYTES

ENCODING_CANDIDATES = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]
SEPARATOR_CANDIDATES = [",", ";", "\t", "|"]


def detect_encoding(path: Path) -> str:
    """Erkennt das Encoding einer CSV-Datei durch Ausprobieren.

    Versucht die gängigsten Encodings der Reihe nach.
    Gibt das erste zurück, das fehlerfrei liest.
    """
    raw = path.read_bytes()[:CSV_SNIFF_BYTES]

    # BOM-Erkennung für UTF-8-BOM
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"

    for enc in ENCODING_CANDIDATES:
        try:
            raw.decode(enc)
            return enc
        except (UnicodeDecodeError, LookupError):
            continue

    return "latin-1"  # Letzter Fallback – decodiert alles


def detect_separator(path: Path, encoding: str = "utf-8") -> str:
    """Erkennt den Separator einer CSV-Datei.

    Nutzt csv.Sniffer und fällt bei Fehlschlag auf Häufigkeitszählung zurück.
    """
    try:
        with open(path, "r", encoding=encoding, errors="replace") as f:
            sample = f.read(CSV_SNIFF_BYTES)
    except OSError:
        return ","

    # Versuch 1: csv.Sniffer
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        if dialect.delimiter in SEPARATOR_CANDIDATES:
            return dialect.delimiter
    except csv.Error:
        pass

    # Versuch 2: Häufigkeitszählung in der ersten Zeile
    first_line = sample.split("\n")[0] if "\n" in sample else sample
    counts = {sep: first_line.count(sep) for sep in SEPARATOR_CANDIDATES}
    best = max(counts, key=counts.get)
    if counts[best] > 0:
        return best

    return ","  # Default-Fallback
