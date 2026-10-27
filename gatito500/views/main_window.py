"""VISTA PRINCIPAL: compone barra lateral, barra superior y el área de contenido."""
import tkinter as tk

from config import strings as S
from config.theme import C
from views.catalog_view import CatalogView
from views.sidebar import Sidebar
from views.widgets import ScrollArea, Surface, TextBlock


class MainWindow:
    def __init__(self, root, model, controller):
        self.root = root
        root.configure(bg=C.page)

        # "shell" agrupa todo el contenido: durante un cambio de tamaño se oculta
        # y se vuelve a mostrar una sola vez, sin ver el redibujado intermedio.
        self.shell = tk.Frame(root, bg=C.page)
        self.shell.pack(fill="both", expand=True)
        self.sidebar = Sidebar(self.shell, model.teacher, on_logout=controller.logout)
        self.sidebar.pack(side="left", fill="y")

        workspace = tk.Frame(self.shell, bg=C.page)
        workspace.pack(side="left", fill="both", expand=True)
        self._build_topbar(workspace)

        self.scroll = ScrollArea(workspace, bg=C.page)
        self.scroll.pack(fill="both", expand=True)
        self.catalog = CatalogView(self.scroll.inner, model, controller)
        self.catalog.pack(fill="x")

        self.activity = self.catalog.activity  # acceso directo para el controlador

        self._resize_job = None
        self._resizing = False
        root.bind("<Configure>", self._on_root_configure, add="+")

    def _on_root_configure(self, event):
        if event.widget is not self.root:
            return
        if not self._resizing:
            self._resizing = True
            self.shell.pack_forget()          # oculta el contenido mientras cambia el tamaño
        if self._resize_job is not None:
            self.root.after_cancel(self._resize_job)
        self._resize_job = self.root.after(120, self._show_content)

    def _show_content(self):
        self._resize_job = None
        self._resizing = False
        self.shell.pack(fill="both", expand=True)  # se dibuja una sola vez, ya con el tamaño final

    def _build_topbar(self, parent):
        top = tk.Frame(parent, bg=C.page, height=74)
        top.pack(side="top", fill="x")
        top.pack_propagate(False)
        bar = tk.Frame(top, bg=C.page)
        bar.pack(fill="both", expand=True, padx=36)
        TextBlock(bar, S.BREADCRUMB, 15, color=C.muted, bg=C.page).pack(side="left")
        badge = Surface(bar, fill=C.sand, radius=5, pad=(10, 4, 10, 4), fit_width=True)
        badge.pack(side="right")
        TextBlock(badge.body, S.ROLE_BADGE, 13, weight=600, color=C.green, bg=C.sand).pack()
        tk.Frame(parent, height=1, bg=C.border).pack(side="top", fill="x")
