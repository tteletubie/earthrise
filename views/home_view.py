from pathlib import Path
import tkinter as tk

import customtkinter as ctk
from PIL import Image

BACKGROUND = "#f6f4ed"
SURFACE = "#fffefa"
BORDER = "#dddcd1"
INK = "#263d34"
GREEN = "#285344"
MUTED = "#728078"
PALE_GREEN = "#e6ede3"
PALE_TAN = "#eeeadb"
ICON_FONT = "Symbols Nerd Font Mono"


class HomeView(ctk.CTkFrame):
    """CustomTkinter implementation of the Home frame from the Figma design."""
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, fg_color=BACKGROUND)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._images: list[ctk.CTkImage] = []
        self._build_sidebar()
        self._build_workspace()

    def _label(self, parent: tk.Misc, text: str, size: int, color: str = INK, weight: str = "normal", **kwargs: object) -> ctk.CTkLabel:
        return ctk.CTkLabel(parent, text=text, text_color=color, font=("Source Sans 3", size, weight), **kwargs)

    def _build_sidebar(self) -> None:
        sidebar = ctk.CTkFrame(self, width=270, corner_radius=0, fg_color=SURFACE, border_width=1, border_color=BORDER)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(1, weight=1)

        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.grid(row=0, column=0, padx=20, pady=(27, 38), sticky="ew")
        ctk.CTkLabel(brand, text="", width=39, height=42, corner_radius=6, fg_color=PALE_GREEN, text_color=GREEN, font=(ICON_FONT, 22)).pack(side="left")
        brand_text = ctk.CTkFrame(brand, fg_color="transparent")
        brand_text.pack(side="left", padx=11)
        self._label(brand_text, "Entre páginas", 20, GREEN, "bold").pack(anchor="w")
        self._label(brand_text, "BANCO DE LIBROS ESCOLAR", 12, MUTED).pack(anchor="w")

        menu = ctk.CTkFrame(sidebar, fg_color="transparent")
        menu.grid(row=1, column=0, padx=20, sticky="new")
        self._label(menu, "ESPACIO ESCOLAR", 12, MUTED, "bold").pack(anchor="w", pady=(0, 8))
        ctk.CTkButton(menu, text="󱉟   Biblioteca", anchor="w", height=46, corner_radius=6, fg_color=PALE_GREEN, hover_color=PALE_GREEN, text_color=INK, font=("Source Sans 3", 15, "bold")).pack(fill="x")

        session = ctk.CTkFrame(sidebar, fg_color="transparent")
        session.grid(row=2, column=0, padx=20, pady=(0, 24), sticky="sew")
        school = ctk.CTkFrame(session, fg_color=BACKGROUND, corner_radius=6)
        school.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(school, text="♙", text_color=GREEN, font=(ICON_FONT, 22)).pack(anchor="w", padx=14, pady=(10, 0))
        self._label(school, "Primaria Los Encinos", 14, INK, "bold").pack(anchor="w", padx=14)
        self._label(school, "Un libro, muchas formas de\naprender.", 12, MUTED, justify="left").pack(anchor="w", padx=14, pady=(0, 12))

        user = ctk.CTkFrame(session, fg_color="transparent")
        user.pack(fill="x", pady=(0, 14))
        ctk.CTkLabel(user, text="MG", width=36, height=36, corner_radius=18, fg_color=PALE_TAN, text_color=INK, font=("Source Sans 3", 13, "bold")).pack(side="left")
        account = ctk.CTkFrame(user, fg_color="transparent")
        account.pack(side="left", padx=10)
        self._label(account, "María García", 14, INK, "bold").pack(anchor="w")
        self._label(account, "Maestro · 2.º A", 12, MUTED).pack(anchor="w")
        self._label(session, "⇥   Cerrar sesión", 14, MUTED).pack(anchor="w")

    def _build_workspace(self) -> None:
        workspace = ctk.CTkFrame(self, fg_color=BACKGROUND, corner_radius=0)
        workspace.grid(row=0, column=1, sticky="nsew")
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(workspace, height=74, fg_color=BACKGROUND, corner_radius=0, border_width=1, border_color=BORDER)
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)
        self._label(top, "Biblioteca escolar  /  Espacio del maestro", 15, MUTED).pack(side="left", padx=36, pady=20)
        self._label(top, "Maestro", 13, GREEN, "bold", fg_color=PALE_TAN, corner_radius=5, padx=10, pady=4).pack(side="right", padx=36)

        content = ctk.CTkScrollableFrame(workspace, fg_color=BACKGROUND, corner_radius=0, scrollbar_button_color="#d6d6ca", scrollbar_button_hover_color="#bfc9bd")
        content.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        content.grid_columnconfigure(0, weight=1)
        inner = ctk.CTkFrame(content, fg_color="transparent")
        inner.grid(row=0, column=0, sticky="ew", padx=32, pady=32)
        inner.grid_columnconfigure(0, weight=1)

        self._label(inner, "Una historia para cada día", 32, INK).grid(row=0, column=0, sticky="w")
        self._label(inner, "Hola, María. Encuentra la próxima lectura para compartir con tu grupo.", 16, MUTED).grid(row=1, column=0, sticky="w", pady=(6, 20))

        filters = ctk.CTkFrame(inner, fg_color="transparent")
        filters.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        filters.grid_columnconfigure(0, weight=1)
        search = ctk.CTkEntry(filters, height=42, placeholder_text="⌕  Buscar por título, autor o palabra clave", fg_color=SURFACE, border_color=BORDER, text_color=INK, placeholder_text_color=MUTED, font=("Source Sans 3", 15))
        search.grid(row=0, column=0, sticky="ew", padx=(0, 14))
        self._combo(filters, "Todos los grados", 208, 1)
        self._combo(filters, "Todas las categorías", 240, 2)

        summary = ctk.CTkFrame(inner, fg_color="transparent")
        summary.grid(row=3, column=0, sticky="ew", pady=(0, 14))
        self._label(summary, "10 libros disponibles", 16, INK, "bold").pack(side="left")
        self._label(summary, "Todos incluyen una actividad", 14, MUTED).pack(side="left", padx=12)
        self._label(summary, "Ordenar: recomendados ⌄", 14, MUTED).pack(side="right")

        cards = ctk.CTkFrame(inner, fg_color="transparent")
        cards.grid(row=4, column=0, sticky="ew")
        self._cards_frame = cards
        self._card_widgets: list[ctk.CTkFrame] = []
        for column in range(4): cards.grid_columnconfigure(column, weight=1, uniform="card")
        self._initial_card_layout = True
        cards.bind("<Configure>", self._layout_cards)
        books = [
            ("La semilla de Luna", "Elena Ríos · 10 min de lectura", "2.º grado", "Naturaleza", "raw_image_2.png"),
            ("El viaje de una gota", "Pablo Montes · 8 min de lectura", "2.º grado", "Ciencia", "raw_image_1.jpeg"),
            ("Un abrazo para erizo", "Lucía Vidal · 7 min de lectura", "1.º grado", "Convivencia", "raw_image_4.jpeg"),
            ("El cielo de Tomás", "Inés Navarro · 12 min de lectura", "3.º grado", "Imaginación", "raw_image_7.jpeg"),
        ]
        for book in books: self._card_widgets.append(self._book_card(cards, *book))
        self.after_idle(self._layout_cards)

        pager = ctk.CTkFrame(inner, fg_color="transparent")
        pager.grid(row=5, column=0, sticky="ew", pady=(14, 14))
        self._label(pager, "Mostrando 1–4 de 10 libros", 14, MUTED).pack(side="left")
        page_buttons = ctk.CTkFrame(pager, fg_color="transparent")
        page_buttons.pack(side="right")
        for text, selected in [("Anterior", False), ("1", True), ("2", False), ("3", False), ("Siguiente", False)]:
            ctk.CTkButton(page_buttons, text=text, width=44 if len(text) == 1 else (74 if text == "Siguiente" else 76), height=34, corner_radius=6, fg_color=GREEN if selected else SURFACE, hover_color=PALE_GREEN, border_width=0 if selected else 1, border_color=BORDER, text_color="white" if selected else GREEN, font=("Source Sans 3", 12, "bold")).pack(side="left", padx=(0, 7))

        guide = ctk.CTkFrame(inner, fg_color=PALE_GREEN, corner_radius=10)
        guide.grid(row=6, column=0, sticky="ew", pady=(0, 8))
        ctk.CTkLabel(guide, text="", text_color=GREEN, font=(ICON_FONT, 24)).pack(side="left", padx=(18, 14), pady=18)
        guide_text = ctk.CTkFrame(guide, fg_color="transparent")
        guide_text.pack(side="left", fill="x", expand=True, pady=20)
        self._label(guide_text, "Del cuento a la conversación", 17, INK, "bold").pack(anchor="w")
        self._label(guide_text, "Cada libro tiene preguntas para imaginar, comprender y compartir ideas.", 12, GREEN, wraplength=560, justify="left").pack(anchor="w", pady=(4, 0))
        self._label(guide, "Elige  →  Proyecta  →  Conversa", 12, INK, "bold").pack(side="right", padx=18)

    def _combo(self, parent: tk.Misc, text: str, width: int, column: int) -> None:
        combo = ctk.CTkComboBox(parent, values=[text], width=width, height=42, state="readonly", fg_color=SURFACE, border_color=BORDER, button_color=SURFACE, button_hover_color=PALE_GREEN, text_color=INK, dropdown_fg_color=SURFACE, dropdown_text_color=INK, font=("Source Sans 3", 15))
        combo.set(text)
        combo.grid(row=0, column=column, sticky="e", padx=(0, 14 if column == 1 else 0))

    def _book_card(self, parent: tk.Misc, title: str, details: str, grade: str, category: str, image_name: str) -> ctk.CTkFrame:
        card = ctk.CTkFrame(parent, fg_color=SURFACE, border_width=1, border_color=BORDER, corner_radius=10)
        card.grid_propagate(True)
        cover_area = ctk.CTkFrame(card, height=250, fg_color=BACKGROUND, corner_radius=5)
        cover_area.pack(fill="x", padx=10, pady=(10, 11))
        cover_area.pack_propagate(False)
        image_path = Path(__file__).parents[1] / "assets" / image_name
        image = Image.open(image_path)
        image_ratio = image.width / image.height
        image_width = min(140, max(1, int(190 * image_ratio)))
        image_height = min(190, max(1, int(image_width / image_ratio)))
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(image_width, image_height))
        self._images.append(ctk_image)
        ctk.CTkLabel(cover_area, text="", image=ctk_image).place(relx=0.5, rely=0.5, anchor="center")
        title_label = self._label(card, title, 14, INK, wraplength=180, justify="left", anchor="w")
        title_label.pack(anchor="w", fill="x", padx=10)
        details_label = self._label(card, details, 12, MUTED, wraplength=180, justify="left", anchor="w")
        details_label.pack(anchor="w", fill="x", padx=10, pady=(3, 8))
        card._title_label = title_label  # type: ignore[attr-defined]
        card._details_label = details_label  # type: ignore[attr-defined]
        tags = ctk.CTkFrame(card, fg_color="transparent")
        tags.pack(fill="x", padx=10, pady=(0, 10))
        self._label(tags, grade, 11, GREEN, "bold", fg_color=PALE_GREEN, corner_radius=5, padx=8, pady=3).pack(side="left")
        self._label(tags, category, 11, GREEN, "bold", fg_color=PALE_TAN, corner_radius=5, padx=8, pady=3).pack(side="left", padx=5)
        ctk.CTkButton(card, text="  Ver libro y leer", height=32, corner_radius=6, fg_color=SURFACE, hover_color=PALE_GREEN, border_width=1, border_color=BORDER, text_color=GREEN, font=(ICON_FONT, 12, "bold")).pack(fill="x", padx=10, pady=(0, 10))
        return card

    def _layout_cards(self, _event: tk.Event | None = None) -> None:
        if not hasattr(self, "_cards_frame"): return
        width = self._cards_frame.winfo_width()
        if self._initial_card_layout:
            columns = 4
            self._initial_card_layout = False
        else:
            columns = 4 if width >= 700 else (2 if width >= 560 else 1)
        for column in range(4): self._cards_frame.grid_columnconfigure(column, weight=0, uniform="")
        for column in range(columns): self._cards_frame.grid_columnconfigure(column, weight=1, uniform="card")
        for index, card in enumerate(self._card_widgets):
            row, column = divmod(index, columns)
            card.grid(row=row, column=column, sticky="nsew", padx=(0 if column == 0 else 6, 6 if column < columns - 1 else 0), pady=(0, 10))