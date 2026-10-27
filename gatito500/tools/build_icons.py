"""Herramienta de desarrollo: convierte assets/icons/*.svg a PNG (4x) para Tkinter.
Uso:  pip install cairosvg  &&  python tools/build_icons.py
Solo hace falta si cambias los SVG. Los PNG ya vienen incluidos."""
from pathlib import Path

import cairosvg

ICONS = Path(__file__).resolve().parents[1] / "assets" / "icons"

for svg in sorted(ICONS.glob("*.svg")):
    cairosvg.svg2png(url=str(svg), write_to=str(svg.with_suffix(".png")), scale=4)
    print("OK", svg.name)
