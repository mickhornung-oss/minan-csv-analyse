"""Text-Hilfsfunktionen: Formatierung von Zahlen und Texten."""


def format_number(value: float, decimals: int = 2) -> str:
    """Formatiert eine Zahl mit Tausender-Punkt und Dezimalkomma (DE-Stil)."""
    formatted = f"{value:,.{decimals}f}"
    # Englisches Format -> deutsches Format
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted


def truncate(text: str, max_length: int = 50) -> str:
    """Kürzt einen Text auf max_length Zeichen mit '...'."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
