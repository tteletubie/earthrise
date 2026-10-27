"""Carga de iconos (SVG convertidos a PNG 4x) e ilustraciones de portada."""
from functools import lru_cache

from PIL import Image, ImageDraw, ImageTk

from config.settings import ICONS_DIR, IMAGES_DIR


@lru_cache(maxsize=None)
def icon(name, size):
    img = Image.open(ICONS_DIR / f"{name}.png").convert("RGBA")
    img = img.resize((size, size), Image.LANCZOS)
    return ImageTk.PhotoImage(img)


@lru_cache(maxsize=None)
def cover_photo(filename, width, height, radius):
    """Equivale a object-fit: cover, con las esquinas inferiores redondeadas."""
    src = Image.open(IMAGES_DIR / filename).convert("RGBA")
    scale = max(width / src.width, height / src.height)
    new_size = (round(src.width * scale), round(src.height * scale))
    src = src.resize(new_size, Image.LANCZOS)
    left = (new_size[0] - width) // 2
    top = (new_size[1] - height) // 2
    img = src.crop((left, top, left + width, top + height))
    mask = Image.new("L", (width, height), 0)
    # Se desplaza hacia arriba para que solo se redondeen las esquinas inferiores
    ImageDraw.Draw(mask).rounded_rectangle((0, -radius * 2, width - 1, height - 1),
                                           radius=radius, fill=255)
    img.putalpha(mask)
    return ImageTk.PhotoImage(img)
