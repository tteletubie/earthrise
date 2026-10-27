"""Registra las fuentes incluidas en assets/fonts (Source Sans 3)."""
import sys
import tkinter.font as tkfont

from config import theme
from config.settings import FONTS_DIR


def register_fonts():
    """Llamar después de crear tk.Tk(). En Windows la fuente se carga solo para esta app."""
    if sys.platform.startswith("win"):
        import ctypes
        gdi32 = ctypes.WinDLL("gdi32")
        FR_PRIVATE = 0x10
        for ttf in sorted(FONTS_DIR.glob("*.ttf")):
            gdi32.AddFontResourceExW(str(ttf), FR_PRIVATE, 0)
    theme.set_available_families(set(tkfont.families()))
