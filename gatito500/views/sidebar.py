"""VISTA: barra lateral (224px), identidad, navegación, escuela, usuario y salir."""
import tkinter as tk

from config import strings as S
from config.theme import C, font
from views import assets
from views.widgets import Surface, TextBlock


class Sidebar(tk.Frame):
    def __init__(self, master, teacher, on_logout):
        super().__init__(master, bg=C.surface, width=224)
        self.pack_propagate(False)
        tk.Frame(self, width=1, bg=C.border).pack(side="right", fill="y")

        inner = tk.Frame(self, bg=C.surface)
        inner.pack(fill="both", expand=True, padx=20, pady=(27, 24))
        bottom = tk.Frame(inner, bg=C.surface)
        bottom.pack(side="bottom", fill="x")
        top = tk.Frame(inner, bg=C.surface)
        top.pack(side="top", fill="x")

        self._build_top(top)
        self._build_bottom(bottom, teacher, on_logout)

    def _build_top(self, top):
        brand = tk.Frame(top, bg=C.surface)
        brand.pack(fill="x")
        logo = Surface(brand, fill=C.sage, radius=6, width=39, height=42)
        logo.pack(side="left")
        tk.Label(
            logo.body,
            image=assets.icon("book-open-1", 25, C.white),
            bg=C.sage,
            bd=0,
        ).pack(expand=True)
        names = tk.Frame(brand, bg=C.surface)
        names.pack(side="left", padx=(11, 0))
        TextBlock(names, S.BRAND_TITLE, 20, weight=700, color=C.ink, bg=C.surface).pack(anchor="w")
        TextBlock(names, S.BRAND_SUBTITLE, 12, color=C.muted, bg=C.surface).pack(anchor="w")

        menu = tk.Frame(top, bg=C.surface)
        menu.pack(fill="x", pady=(38, 0))
        TextBlock(menu, S.SECTION_LABEL, 12, weight=600, color=C.muted, bg=C.surface).pack(anchor="w")
        nav = Surface(menu, fill=C.sage, radius=6, height=46, pad=(11, 0, 11, 0))
        nav.pack(fill="x", pady=(8, 0))
        tk.Label(nav.body, image=assets.icon("library", 20), bg=C.sage, bd=0).pack(side="left")
        TextBlock(nav.body, S.NAV_LIBRARY, 15, weight=600, color=C.ink,
                  bg=C.sage).pack(side="left", padx=(10, 0))

    def _build_bottom(self, bottom, teacher, on_logout):
        school = Surface(bottom, fill=C.page, radius=6, pad=(14, 14, 14, 14))
        school.pack(fill="x", pady=(0, 20))
        tk.Label(school.body, image=assets.icon("school", 22), bg=C.page, bd=0).pack(anchor="w")
        TextBlock(school.body, S.SCHOOL_NAME, 14, weight=600, color=C.ink, mode="fill",
                  lh=1.35, bg=C.page).pack(fill="x", pady=(6, 0))
        TextBlock(school.body, S.SCHOOL_MOTTO, 12, color=C.muted, mode="fill",
                  lh=1.35, bg=C.page).pack(fill="x", pady=(6, 0))

        user = tk.Frame(bottom, bg=C.surface)
        user.pack(fill="x", pady=(0, 20))
        avatar = tk.Canvas(user, width=36, height=36, bg=C.surface, highlightthickness=0, bd=0)
        avatar.create_oval(0, 0, 36, 36, fill=C.sand, outline="")
        avatar.create_text(18, 18, text=teacher["initials"], font=font(13, 700), fill=C.ink)
        avatar.pack(side="left")
        info = tk.Frame(user, bg=C.surface)
        info.pack(side="left", padx=(10, 0))
        TextBlock(info, teacher["name"], 14, weight=600, color=C.ink, bg=C.surface).pack(anchor="w")
        TextBlock(info, teacher["role"], 12, color=C.muted, bg=C.surface).pack(anchor="w")

        logout = tk.Frame(bottom, bg=C.surface, cursor="hand2")
        logout.pack(fill="x")
        icon_label = tk.Label(logout, image=assets.icon("log-out", 17), bg=C.surface, bd=0)
        icon_label.pack(side="left")
        text = TextBlock(logout, S.LOGOUT, 14, color=C.muted, bg=C.surface)
        text.pack(side="left", padx=(9, 0))
        for widget in (logout, icon_label, text):
            widget.bind("<Button-1>", lambda _e: on_logout())
