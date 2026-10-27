"""Punto de entrada de GATITO500 (Entre páginas · banco de libros escolar).

F11: pantalla completa (sin barra de título). Esc: salir de pantalla completa.
"""
import sys
import tkinter as tk

from config.settings import APP_TITLE, INITIAL_SCREEN_RATIO, MIN_WINDOW_SIZE
from controllers.app_controller import AppController
from views.fonts import register_fonts


def _enable_dpi_awareness():
    """En Windows evita que la ventana se vea borrosa o escalada con 125%/150%."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass


def main():
    _enable_dpi_awareness()
    root = tk.Tk()
    root.title(APP_TITLE)
    register_fonts()

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    w = int(screen_w * INITIAL_SCREEN_RATIO[0])
    h = int(screen_h * INITIAL_SCREEN_RATIO[1])
    root.geometry(f"{w}x{h}+{(screen_w - w) // 2}+{(screen_h - h) // 2}")
    root.minsize(*MIN_WINDOW_SIZE)

    # Se construye invisible (opacidad 0) y se muestra ya dibujada: nunca se ve el armado
    _set_alpha(root, 0.0)
    root.withdraw()
    AppController(root)
    root.update()
    root.deiconify()
    root.update()
    _set_alpha(root, 1.0)
    root.mainloop()


def _set_alpha(root, value):
    try:
        root.attributes("-alpha", value)
    except tk.TclError:
        pass  # algunas plataformas no soportan opacidad: no pasa nada


if __name__ == "__main__":
    main()
