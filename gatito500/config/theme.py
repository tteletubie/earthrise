"""Colores y tipografía del CSS original. Los tamaños son píxeles, igual que en la web."""


class C:
    page = "#f6f4ed"      # fondo general
    surface = "#fffefa"   # tarjetas, sidebar, campos
    border = "#dddcd1"
    sand = "#eeeadb"
    sage = "#e6ede3"
    cream = "#f5ebd4"
    mist = "#e5edef"
    blush = "#f5e8e0"
    ink = "#263d34"       # texto principal
    green = "#285344"     # acentos y texto de botones
    muted = "#728078"     # texto secundario
    white = "#ffffff"


FAMILY = "Source Sans 3"
FAMILY_SEMIBOLD = "Source Sans 3 SemiBold"
_semibold_available = False


def set_available_families(names):
    """Se llama al arrancar, cuando ya se registraron las fuentes incluidas."""
    global _semibold_available
    _semibold_available = FAMILY_SEMIBOLD in names


def font(px, weight=400):
    """Especificación de fuente Tk. Tamaño negativo = píxeles (como el CSS)."""
    if weight >= 700:
        return (FAMILY, -px, "bold")
    if weight >= 600:
        if _semibold_available:
            return (FAMILY_SEMIBOLD, -px)
        return (FAMILY, -px, "bold")
    return (FAMILY, -px)
