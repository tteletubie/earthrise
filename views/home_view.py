from io import BytesIO
from pathlib import Path
import tkinter as tk

import cairosvg
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

    def _label(
        self,
        parent: tk.Misc,
        text: str,
        size: int,
        color: str = INK,
        weight: str = "normal",
        **kwargs: object,
    ) -> ctk.CTkLabel:
        return ctk.CTkLabel(
            parent,
            text=text,
            text_color=color,
            font=("Source Sans 3", size, weight),
            **kwargs,
        )

    def _build_sidebar(self) -> None:
        sidebar = ctk.CTkFrame(
            self,
            width=224,
            fg_color=SURFACE,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        inner = ctk.CTkFrame(sidebar, fg_color="transparent", corner_radius=0)
        inner.pack(fill="both", expand=True, padx=20, pady=(27, 24))

        top = ctk.CTkFrame(inner, fg_color="transparent", corner_radius=0)
        top.pack(fill="x", side="top")

        brand = ctk.CTkFrame(top, fg_color="transparent", corner_radius=0)
        brand.pack(fill="x")
        logo = ctk.CTkFrame(
            brand, width=39, height=45, fg_color="#E6EDE3", corner_radius=9
        )
        logo.pack(side="left")
        logo.pack_propagate(False)
        self._sidebar_svg_icon(logo, "book-open-1", 25, "transparent", GREEN).pack(
            expand=True
        )

        names = ctk.CTkFrame(brand, fg_color="transparent", corner_radius=0)
        names.pack(side="left", padx=(11, 0))
        self._label(names, "Entre páginas", 20, INK, "bold", height=24).pack(anchor="w")
        self._label(names, "BANCO DE LIBROS ESCOLAR", 12, MUTED, height=20).pack(anchor="w")

        menu = ctk.CTkFrame(top, fg_color="transparent", corner_radius=0)
        menu.pack(fill="x", pady=(38, 0))
        self._label(menu, "ESPACIO ESCOLAR", 12, MUTED, "bold").pack(anchor="w")

        navigation = ctk.CTkFrame(menu, height=46, fg_color=PALE_GREEN, corner_radius=6)
        navigation.pack(fill="x", pady=(8, 0))
        navigation.pack_propagate(False)
        self._sidebar_svg_icon(navigation, "library", 20, "transparent", GREEN).pack(
            side="left", padx=(11, 0)
        )
        self._label(navigation, "Biblioteca", 15, INK, "bold").pack(
            side="left", padx=(10, 0)
        )

        bottom = ctk.CTkFrame(inner, fg_color="transparent", corner_radius=0)
        bottom.pack(fill="x", side="bottom")

        school = ctk.CTkFrame(bottom, fg_color=BACKGROUND, corner_radius=6)
        school.pack(fill="x", pady=(0, 20))
        self._sidebar_svg_icon(school, "school", 22, "transparent", GREEN).pack(
            anchor="w", padx=14, pady=(14, 0)
        )
        self._label(
            school,
            "Primaria Justicia Social",
            14,
            INK,
            "bold",
            wraplength=156,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=14, pady=(6, 0))
        self._label(
            school,
            "Un libro, muchas formas de aprender.",
            12,
            MUTED,
            wraplength=156,
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=14, pady=(6, 14))

        user = ctk.CTkFrame(bottom, fg_color="transparent", corner_radius=0)
        user.pack(fill="x", pady=(0, 20))
        avatar = tk.Canvas(
            user,
            width=36,
            height=36,
            bg=SURFACE,
            highlightthickness=0,
            bd=0,
        )
        avatar.create_oval(1, 1, 35, 35, fill=PALE_TAN, outline="")
        avatar.create_text(18, 18, text="MG", fill=INK, font=("Source Sans 3", 10, "bold"))
        avatar.pack(side="left")
        info = ctk.CTkFrame(user, fg_color="transparent", corner_radius=0)
        info.pack(side="left", padx=(10, 0))
        self._label(info, "María García", 14, INK, "bold", height=20).pack(anchor="w")
        self._label(info, "Maestra · 2° A", 12, MUTED, height=18).pack(anchor="w")

        logout = ctk.CTkFrame(
            bottom, fg_color="transparent", corner_radius=0, cursor="hand2"
        )
        logout.pack(fill="x")
        self._sidebar_svg_icon(logout, "log-out", 17, "transparent", MUTED).pack(
            side="left"
        )
        self._label(logout, "Cerrar sesión", 14, MUTED).pack(side="left", padx=(9, 0))

    def _sidebar_svg_icon(
        self,
        parent: tk.Misc,
        name: str,
        size: int,
        background: str,
        color: str,
    ) -> ctk.CTkLabel:
        image_path = (
            Path(__file__).parents[1] / "gatito500" / "assets" / "icons" / f"{name}.svg"
        )
        svg = image_path.read_text(encoding="utf-8")
        for source_color in ("#285344", "#728078"):
            svg = svg.replace(source_color, color)
        rendered = cairosvg.svg2png(
            bytestring=svg.encode("utf-8"),
            output_width=size,
            output_height=size,
        )
        source = Image.open(BytesIO(rendered)).convert("RGBA")
        image = ctk.CTkImage(
            light_image=source,
            dark_image=source,
            size=(size, size),
        )
        self._images.append(image)
        return ctk.CTkLabel(parent, text="", image=image, fg_color=background)

    def _build_workspace(self) -> None:
        workspace = ctk.CTkFrame(self, fg_color=BACKGROUND, corner_radius=0)
        workspace.grid(row=0, column=1, sticky="nsew")
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(
            workspace,
            height=74,
            fg_color=BACKGROUND,
            corner_radius=0,
            border_width=0,
            border_color=BORDER,
        )
        bottom_border = ctk.CTkFrame(
            top,
            height=1,
            border_width=1,
            fg_color=BORDER,
            corner_radius=0,
        )
        bottom_border.pack(side="bottom", fill="x")
        top.grid(row=0, column=0, sticky="ew")
        top.grid_propagate(False)
        self._label(top, "Biblioteca escolar  /  Espacio del maestro", 15, MUTED).pack(
            side="left", padx=36, pady=20
        )
        self._label(
            top,
            "Maestro",
            13,
            GREEN,
            "bold",
            fg_color=PALE_TAN,
            corner_radius=5,
            padx=10,
            pady=4,
        ).pack(side="right", padx=36)

        content = ctk.CTkScrollableFrame(
            workspace,
            fg_color=BACKGROUND,
            corner_radius=0,
            scrollbar_button_color="#d6d6ca",
            scrollbar_button_hover_color="#bfc9bd",
        )
        content.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        content.grid_columnconfigure(0, weight=1)
        inner = ctk.CTkFrame(content, fg_color="transparent")
        inner.grid(row=0, column=0, sticky="ew", padx=32, pady=32)
        inner.grid_columnconfigure(0, weight=1)

        self._label(inner, "Una historia para cada día", 32, INK).grid(
            row=0, column=0, sticky="w"
        )
        self._label(
            inner,
            "Hola, María. Encuentra la próxima lectura para compartir con tu grupo.",
            16,
            MUTED,
        ).grid(row=1, column=0, sticky="w", pady=(6, 20))

        filters = ctk.CTkFrame(inner, fg_color="transparent")
        filters.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        filters.grid_columnconfigure(0, weight=1)
        search = ctk.CTkEntry(
            filters,
            height=42,
            placeholder_text="⌕  Buscar por título, autor o palabra clave",
            fg_color=SURFACE,
            border_color=BORDER,
            text_color=INK,
            placeholder_text_color=MUTED,
            font=("Source Sans 3", 15),
        )
        search.grid(row=0, column=0, sticky="ew", padx=(0, 14))
        self._combo(filters, "Todos los grados", 208, 1)
        self._combo(filters, "Todas las categorías", 240, 2)

        summary = ctk.CTkFrame(inner, fg_color="transparent")
        summary.grid(row=3, column=0, sticky="ew", pady=(0, 14))
        self._label(summary, "10 libros disponibles", 16, INK, "bold").pack(side="left")
        self._label(summary, "Todos incluyen una actividad", 14, MUTED).pack(
            side="left", padx=12
        )
        self._label(summary, "Ordenar: recomendados ⌄", 14, MUTED).pack(side="right")

        cards = ctk.CTkFrame(inner, fg_color="transparent")
        cards.grid(row=4, column=0, sticky="ew")
        self._cards_frame = cards
        self._card_widgets: list[ctk.CTkFrame] = []
        for column in range(4):
            cards.grid_columnconfigure(column, weight=1, uniform="card")
        self._initial_card_layout = True
        cards.bind("<Configure>", self._layout_cards)
        books = [
            (
                "La semilla de Luna",
                "Elena Ríos · 10 min de lectura",
                "2.º grado",
                "Naturaleza",
                "raw_image_2.png",
            ),
            (
                "El viaje de una gota",
                "Pablo Montes · 8 min de lectura",
                "2.º grado",
                "Ciencia",
                "raw_image_1.jpeg",
            ),
            (
                "Un abrazo para erizo",
                "Lucía Vidal · 7 min de lectura",
                "1.º grado",
                "Convivencia",
                "raw_image_4.jpeg",
            ),
            (
                "El cielo de Tomás",
                "Inés Navarro · 12 min de lectura",
                "3.º grado",
                "Imaginación",
                "raw_image_7.jpeg",
            ),
        ]
        for book in books:
            self._card_widgets.append(self._book_card(cards, *book))
        self.after_idle(self._layout_cards)

        pager = ctk.CTkFrame(inner, fg_color="transparent")
        pager.grid(row=5, column=0, sticky="ew", pady=(14, 14))
        self._label(pager, "Mostrando 1–4 de 10 libros", 14, MUTED).pack(side="left")
        page_buttons = ctk.CTkFrame(pager, fg_color="transparent")
        page_buttons.pack(side="right")
        for text, selected in [
            ("Anterior", False),
            ("1", True),
            ("2", False),
            ("3", False),
            ("Siguiente", False),
        ]:
            ctk.CTkButton(
                page_buttons,
                text=text,
                width=44 if len(text) == 1 else (74 if text == "Siguiente" else 76),
                height=34,
                corner_radius=6,
                fg_color=GREEN if selected else SURFACE,
                hover_color=PALE_GREEN,
                border_width=0 if selected else 1,
                border_color=BORDER,
                text_color="white" if selected else GREEN,
                font=("Source Sans 3", 12, "bold"),
            ).pack(side="left", padx=(0, 7))

        guide = ctk.CTkFrame(inner, fg_color=PALE_GREEN, corner_radius=10)
        guide.grid(row=6, column=0, sticky="ew", pady=(0, 8))
        ctk.CTkLabel(guide, text="", text_color=GREEN, font=(ICON_FONT, 24)).pack(
            side="left", padx=(18, 14), pady=18
        )
        guide_text = ctk.CTkFrame(guide, fg_color="transparent")
        guide_text.pack(side="left", fill="x", expand=True, pady=20)
        self._label(guide_text, "Del cuento a la conversación", 17, INK, "bold").pack(
            anchor="w"
        )
        self._label(
            guide_text,
            "Cada libro tiene preguntas para imaginar, comprender y compartir ideas.",
            12,
            GREEN,
            wraplength=560,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))
        self._label(guide, "Elige  →  Proyecta  →  Conversa", 12, INK, "bold").pack(
            side="right", padx=18
        )

    def _combo(self, parent: tk.Misc, text: str, width: int, column: int) -> None:
        combo = ctk.CTkComboBox(
            parent,
            values=[text],
            width=width,
            height=42,
            state="readonly",
            fg_color=SURFACE,
            border_color=BORDER,
            button_color=SURFACE,
            button_hover_color=PALE_GREEN,
            text_color=INK,
            dropdown_fg_color=SURFACE,
            dropdown_text_color=INK,
            font=("Source Sans 3", 15),
        )
        combo.set(text)
        combo.grid(row=0, column=column, sticky="e", padx=(0, 14 if column == 1 else 0))

    def _book_card(
        self,
        parent: tk.Misc,
        title: str,
        details: str,
        grade: str,
        category: str,
        image_name: str,
    ) -> ctk.CTkFrame:
        card = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
            corner_radius=10,
        )
        card.grid_propagate(True)
        cover_area = ctk.CTkFrame(
            card, height=250, fg_color=BACKGROUND, corner_radius=5
        )
        cover_area.pack(fill="x", padx=10, pady=(10, 11))
        cover_area.pack_propagate(False)
        image_path = Path(__file__).parents[1] / "assets" / image_name
        image = Image.open(image_path)
        image_ratio = image.width / image.height
        image_width = min(140, max(1, int(190 * image_ratio)))
        image_height = min(190, max(1, int(image_width / image_ratio)))
        ctk_image = ctk.CTkImage(
            light_image=image, dark_image=image, size=(image_width, image_height)
        )
        self._images.append(ctk_image)
        ctk.CTkLabel(cover_area, text="", image=ctk_image).place(
            relx=0.5, rely=0.5, anchor="center"
        )
        title_label = self._label(
            card, title, 14, INK, wraplength=180, justify="left", anchor="w"
        )
        title_label.pack(anchor="w", fill="x", padx=10)
        details_label = self._label(
            card, details, 12, MUTED, wraplength=180, justify="left", anchor="w"
        )
        details_label.pack(anchor="w", fill="x", padx=10, pady=(3, 8))
        card._title_label = title_label  # type: ignore[attr-defined]
        card._details_label = details_label  # type: ignore[attr-defined]
        tags = ctk.CTkFrame(card, fg_color="transparent")
        tags.pack(fill="x", padx=10, pady=(0, 10))
        self._label(
            tags,
            grade,
            11,
            GREEN,
            "bold",
            fg_color=PALE_GREEN,
            corner_radius=5,
            padx=8,
            pady=3,
        ).pack(side="left")
        self._label(
            tags,
            category,
            11,
            GREEN,
            "bold",
            fg_color=PALE_TAN,
            corner_radius=5,
            padx=8,
            pady=3,
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            card,
            text="  Ver libro y leer",
            height=32,
            corner_radius=6,
            fg_color=SURFACE,
            hover_color=PALE_GREEN,
            border_width=1,
            border_color=BORDER,
            text_color=GREEN,
            font=(ICON_FONT, 12, "bold"),
        ).pack(fill="x", padx=10, pady=(0, 10))
        return card

    def _layout_cards(self, _event: tk.Event | None = None) -> None:
        if not hasattr(self, "_cards_frame"):
            return
        width = self._cards_frame.winfo_width()
        if self._initial_card_layout:
            columns = 4
            self._initial_card_layout = False
        else:
            columns = 4 if width >= 700 else (2 if width >= 560 else 1)
        for column in range(4):
            self._cards_frame.grid_columnconfigure(column, weight=0, uniform="")
        for column in range(columns):
            self._cards_frame.grid_columnconfigure(column, weight=1, uniform="card")
        for index, card in enumerate(self._card_widgets):
            row, column = divmod(index, columns)
            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=(0 if column == 0 else 6, 6 if column < columns - 1 else 0),
                pady=(0, 10),
            )
