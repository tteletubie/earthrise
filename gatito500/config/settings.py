"""Rutas y parámetros generales de la aplicación."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
ICONS_DIR = ASSETS_DIR / "icons"
FONTS_DIR = ASSETS_DIR / "fonts"

APP_TITLE = "Entre páginas · GATITO500"

# La ventana NO usa 1280x960. Al abrir ocupa una proporción de la pantalla
# y el diseño se adapta al tamaño real. F11 pasa a pantalla completa.
INITIAL_SCREEN_RATIO = (0.8, 0.85)
MIN_WINDOW_SIZE = (960, 600)

BOOKS_PER_PAGE = 4
TOTAL_CATALOG_BOOKS = 10
