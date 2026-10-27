"""Componentes personalizados sobre tk.Canvas que reproducen las cajas, botones
y textos del HTML: esquinas redondeadas, bordes de 1px e interlineado de CSS.

Regla de rendimiento: cada elemento crea sus dibujos una sola vez y después solo
actualiza coordenadas o colores, y únicamente cuando cambia su tamaño o su contenido.
Así no hay parpadeo al hacer clic, al pasar el mouse o al maximizar."""
import math
import tkinter as tk
import tkinter.font as tkfont

from config.theme import C, font
from views import assets

_font_cache = {}


def tk_font(spec):
    if spec not in _font_cache:
        weight = spec[2] if len(spec) > 2 else "normal"
        _font_cache[spec] = tkfont.Font(family=spec[0], size=spec[1], weight=weight)
    return _font_cache[spec]


def wrap_lines(text, spec, max_width):
    f = tk_font(spec)
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}" if line else word
            if line and f.measure(candidate) > max_width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines


def _rrect_points(w, h, radius, outlined):
    # Coordenadas enteras: con 0.5 Tk recortaba la última línea del borde
    if outlined:
        x1, y1, x2, y2 = 0, 0, w - 1, h - 1
    else:
        x1, y1, x2, y2 = 0, 0, w, h
    r = max(0, min(radius, (x2 - x1) / 2, (y2 - y1) / 2))
    if r < 1:
        return [x1, y1, x2, y1, x2, y2, x1, y2], False
    pts = [x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y1 + r,
           x2, y2 - r, x2, y2 - r, x2, y2, x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2,
           x1, y2, x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1]
    return pts, True


def draw_rrect(canvas, item, w, h, radius, fill="", outline=""):
    """Crea el rectángulo redondeado la primera vez y después solo mueve/recolorea."""
    pts, smooth = _rrect_points(w, h, radius, bool(outline))
    if item is None:
        item = canvas.create_polygon(pts, smooth=smooth, fill=fill, outline=outline, width=1)
        canvas.tag_lower(item)
    else:
        canvas.coords(item, *pts)
        canvas.itemconfigure(item, fill=fill, outline=outline, smooth=smooth)
    return item


class Surface(tk.Canvas):
    """Caja con fondo, borde y esquinas redondeadas. Su contenido va en self.body.
    fit_width=True: el ancho se ajusta al contenido (etiquetas y píldoras)."""

    def __init__(self, master, *, fill=C.surface, border=None, radius=10, pad=(0, 0, 0, 0),
                 width=None, height=None, fit_width=False, bg=None):
        super().__init__(master, bg=bg or master.cget("bg"), highlightthickness=0, bd=0,
                         width=width or 1, height=height or 1)
        self.fill_color = fill
        self.border = border
        self.radius = radius
        self.pad = pad
        self._fixed_height = height is not None
        self._fit_width = fit_width
        self._bg_item = None
        self._size = None
        self.body = tk.Frame(self, bg=fill)
        self._win = self.create_window(pad[0], pad[1], anchor="nw", window=self.body)
        self.body.bind("<Configure>", self._relayout)
        self.bind("<Configure>", self._relayout)

    def _relayout(self, _event=None):
        pl, pt, pr, pb = self.pad
        kwargs = {}
        if self._fit_width:
            wanted_w = self.body.winfo_reqwidth() + pl + pr
            if self.winfo_width() != wanted_w:
                kwargs["width"] = wanted_w
        if not self._fixed_height:
            wanted_h = self.body.winfo_reqheight() + pt + pb
            if self.winfo_height() != wanted_h:
                kwargs["height"] = wanted_h
        if kwargs:
            self.configure(**kwargs)
        self._draw()

    def _draw(self):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 2 or h < 1 or (w, h) == self._size:
            return
        self._size = (w, h)
        self._bg_item = draw_rrect(self, self._bg_item, w, h, self.radius,
                                   self.fill_color, self.border or "")
        pl, pt, pr, pb = self.pad
        options = {"width": max(1, w - pl - pr)}
        if self._fixed_height:
            options["height"] = max(1, h - pt - pb)
        self.itemconfigure(self._win, **options)


VARIANTS = {
    "outline": {"fill": C.surface, "hover": C.page, "border": C.border, "fg": C.green},
    "ghost": {"fill": C.page, "hover": C.sand, "border": "", "fg": C.green},
    "solid": {"fill": C.green, "hover": C.ink, "border": "", "fg": C.white},
}


class RoundedButton(tk.Canvas):
    """Botón redondeado. blank_icon reserva el hueco de un <img> sin src del HTML."""

    def __init__(self, master, text, command=None, *, variant="outline", height=34, px=15,
                 weight=600, radius=6, padx=12, gap=8, icon=None, icon_size=17,
                 blank_icon=False, expand=False, bg=None):
        self._text = text
        self._command = command
        self._spec = font(px, weight)
        self._variant = VARIANTS[variant]
        self._icon = assets.icon(icon, icon_size) if icon else None
        self._icon_size = icon_size
        self._lead = (icon_size + gap) if (icon or blank_icon) else 0
        self._padx = padx
        self._radius = radius
        self._expand = expand
        self._hover = False
        self._poly = None
        self._key = None
        super().__init__(master, height=height, bg=bg or master.cget("bg"),
                         highlightthickness=0, bd=0, cursor="hand2", width=1)
        if not expand:
            self.configure(width=self._natural_width())
        self.bind("<Configure>", lambda _e: self._draw())
        self.bind("<Enter>", lambda _e: self._set_hover(True))
        self.bind("<Leave>", lambda _e: self._set_hover(False))
        self.bind("<ButtonRelease-1>", self._click)

    def _natural_width(self):
        return 2 * self._padx + self._lead + tk_font(self._spec).measure(self._text)

    def _state_fill(self):
        return self._variant["hover"] if self._hover else self._variant["fill"]

    def _click(self, _event):
        if self._command:
            self._command()

    def _set_hover(self, on):
        self._hover = on
        if self._poly is not None:  # solo cambia el color, sin redibujar todo
            self.itemconfigure(self._poly, fill=self._state_fill())

    def set_variant(self, name):
        if VARIANTS[name] is self._variant:
            return
        self._variant = VARIANTS[name]
        self._draw(force=True)

    def set_text(self, text):
        if text == self._text:
            return
        self._text = text
        if not self._expand:
            self.configure(width=self._natural_width())
        self._draw(force=True)

    def _draw(self, force=False):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 2:
            return
        key = (w, h, self._text, id(self._variant))
        if key == self._key and not force:
            return
        self._key = key
        self._poly = draw_rrect(self, self._poly, w, h, self._radius, self._state_fill(),
                                self._variant["border"])
        self.delete("content")
        total = self._lead + tk_font(self._spec).measure(self._text)
        x = (w - total) / 2
        cy = h / 2
        if self._icon is not None:
            self.create_image(x + self._icon_size / 2, cy, image=self._icon, tags="content")
        self.create_text(x + self._lead, cy, text=self._text, anchor="w", font=self._spec,
                         fill=self._variant["fg"], tags="content")


class TextBlock(tk.Canvas):
    """Texto dibujado línea a línea con el line-height del CSS.
    mode='natural': ancho = texto. mode='fill': ocupa el ancho disponible.
    mode='fixed': ancho dado en `wrap`."""

    def __init__(self, master, text, px, *, weight=400, color=C.ink, lh=1.257,
                 mode="natural", wrap=None, bg=None):
        self._text = text
        self._spec = font(px, weight)
        self._color = color
        self._line = px * lh
        self._mode = mode
        self._wrap = wrap
        self._key = None
        super().__init__(master, bg=bg or master.cget("bg"), highlightthickness=0, bd=0,
                         width=1, height=1)
        self.bind("<Configure>", lambda _e: self._draw())
        self._draw()

    def set_text(self, text):
        if text != self._text:
            self._text = text
            self._draw()

    def _draw(self):
        if self._mode == "fill":
            width = self.winfo_width()
            if width < 2:
                return
        elif self._mode == "fixed":
            width = self._wrap
        else:
            width = None
        key = (width, self._text)
        if key == self._key:
            return
        self._key = key

        if width is None:
            lines = self._text.split("\n")
            width = max(tk_font(self._spec).measure(line) for line in lines)
        else:
            lines = wrap_lines(self._text, self._spec, width)
        height = math.ceil(len(lines) * self._line)
        if self._mode != "fill":
            self.configure(width=width)
        if int(self.cget("height")) != height:
            self.configure(height=height)
        self.delete("all")
        for i, line in enumerate(lines):
            self.create_text(0, i * self._line + self._line / 2, text=line, anchor="w",
                             font=self._spec, fill=self._color)


class SelectBox(Surface):
    """Campo desplegable con el mismo aspecto que el <div> del HTML."""

    def __init__(self, master, options, value, on_change, width):
        super().__init__(master, fill=C.surface, border=C.border, radius=6,
                         pad=(13, 0, 13, 0), width=width, height=42)
        self._on_change = on_change
        self._label = TextBlock(self.body, value, 15, color=C.muted, mode="fill", bg=C.surface)
        self._label.pack(side="left", fill="x", expand=True)
        chevron = tk.Label(self.body, image=assets.icon("chevron-down", 16), bg=C.surface, bd=0)
        chevron.pack(side="right")
        self._menu = tk.Menu(self, tearoff=0, bg=C.surface, fg=C.ink, bd=0,
                             activebackground=C.sage, activeforeground=C.ink, font=font(15))
        for option in options:
            self._menu.add_command(label=option, command=lambda o=option: self._choose(o))
        for widget in (self, self.body, self._label, chevron):
            widget.bind("<Button-1>", self._open)

    def _open(self, _event):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        try:
            self._menu.tk_popup(x, y)
        finally:
            self._menu.grab_release()

    def _choose(self, option):
        self._label.set_text(option)
        self._on_change(option)


class SearchField(Surface):
    """Campo de búsqueda con icono y texto de ayuda (placeholder)."""

    def __init__(self, master, placeholder, on_change):
        super().__init__(master, fill=C.surface, border=C.border, radius=6,
                         pad=(13, 0, 13, 0), height=42)
        self._placeholder = placeholder
        self._on_change = on_change
        self._is_placeholder = True
        tk.Label(self.body, image=assets.icon("search", 18), bg=C.surface, bd=0).pack(
            side="left", padx=(0, 10))
        self._var = tk.StringVar(value=placeholder)
        self._entry = tk.Entry(self.body, textvariable=self._var, bd=0, relief="flat",
                               highlightthickness=0, bg=C.surface, fg=C.muted,
                               insertbackground=C.green, font=font(15))
        self._entry.pack(side="left", fill="x", expand=True)
        self._entry.bind("<FocusIn>", self._focus_in)
        self._entry.bind("<FocusOut>", self._focus_out)
        self._var.trace_add("write", self._written)

    def _focus_in(self, _event):
        if self._is_placeholder:
            self._is_placeholder = False
            self._entry.configure(fg=C.ink)
            self._var.set("")

    def _focus_out(self, _event):
        if not self._var.get():
            self._is_placeholder = True
            self._entry.configure(fg=C.muted)
            self._var.set(self._placeholder)
            self._on_change("")

    def _written(self, *_args):
        if not self._is_placeholder:
            self._on_change(self._var.get())


class ScrollArea(tk.Frame):
    """Área de contenido desplazable con la rueda del ratón (sin barra visible)."""

    def __init__(self, master, bg):
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self._window = self.canvas.create_window(0, 0, anchor="nw", window=self.inner)
        self.inner.bind("<Configure>", self._sync)
        self.canvas.bind("<Configure>", self._sync)
        self.bind_all("<MouseWheel>", self._on_wheel, add="+")
        self.bind_all("<Button-4>", self._on_wheel, add="+")
        self.bind_all("<Button-5>", self._on_wheel, add="+")

    def _sync(self, _event=None):
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        content_h = self.inner.winfo_reqheight()
        self.canvas.itemconfigure(self._window, width=cw)
        self.canvas.configure(scrollregion=(0, 0, cw, max(ch, content_h)))

    def _pointer_inside(self, event):
        try:
            widget = self.winfo_containing(event.x_root, event.y_root)
        except KeyError:
            return False
        while widget is not None:
            if widget is self:
                return True
            widget = widget.master
        return False

    def _on_wheel(self, event):
        if not self._pointer_inside(event):
            return
        if event.num == 4:
            step = -1
        elif event.num == 5:
            step = 1
        else:
            step = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(step, "units")


def Spacer(master, width, height, bg):
    """Hueco de tamaño fijo (equivale a un <img> sin src con tamaño definido)."""
    frame = tk.Frame(master, width=width, height=height, bg=bg)
    frame.pack_propagate(False)
    return frame
