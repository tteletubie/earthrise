"""VISTA: catálogo de lecturas (encabezado, filtros, tarjetas, paginación y guía)."""
import tkinter as tk

from config import strings as S
from config.theme import C, font
from views import assets
from views.activity_view import ActivityView
from views.widgets import (RoundedButton, SearchField, SelectBox, Surface, TextBlock,
                           draw_rrect, wrap_lines)


class CoverWidget(tk.Canvas):
    """Portada 160x230: título y autor arriba, ilustración abajo (object-fit: cover)."""
    WIDTH, HEIGHT, RADIUS = 160, 230, 5

    def __init__(self, master, book):
        super().__init__(master, width=self.WIDTH, height=self.HEIGHT, bg=master.cget("bg"),
                         highlightthickness=0, bd=0)
        draw_rrect(self, None, self.WIDTH, self.HEIGHT, self.RADIUS, fill=book["cover_bg"])
        title_font = font(18, 700)
        title_lh = 18 * 1.08
        lines = wrap_lines(book["title"], title_font, 136)
        y = 14
        for line in lines:
            self.create_text(12, y, text=line, anchor="nw", font=title_font, fill=C.ink)
            y += title_lh
        y += 5
        self.create_text(12, y, text=book["author"], anchor="nw", font=font(11), fill=C.green)
        y += 11 * 1.35 + 10
        top = round(y)
        self._photo = assets.cover_photo(book["image"], self.WIDTH, self.HEIGHT - top, self.RADIUS)
        self.create_image(0, top, anchor="nw", image=self._photo)


class BookCard(Surface):
    def __init__(self, master, book, on_open):
        super().__init__(master, fill=C.surface, border=C.border, radius=10, pad=(14, 14, 14, 14))
        presentation = Surface(self.body, fill=C.page, radius=5, pad=(10, 10, 10, 10))
        presentation.pack(fill="x")
        CoverWidget(presentation.body, book).pack()

        ficha = tk.Frame(self.body, bg=C.surface)
        ficha.pack(fill="x", pady=(11, 0))
        TextBlock(ficha, book["title"], 19, color=C.ink, mode="fill", lh=1.35,
                  bg=C.surface).pack(fill="x")
        TextBlock(ficha, f'{book["author"]} · {book["minutes"]} min de lectura', 14,
                  color=C.muted, mode="fill", lh=1.35, bg=C.surface).pack(fill="x", pady=(3, 0))

        tags = tk.Frame(self.body, bg=C.surface)
        tags.pack(fill="x", pady=(11, 0))
        for i, (text, fill) in enumerate([(book["grade"], C.sage), (book["category"], C.sand)]):
            pill = Surface(tags, fill=fill, radius=5, pad=(10, 4, 10, 4), fit_width=True)
            pill.pack(side="left", padx=(0 if i == 0 else 7, 0))
            TextBlock(pill.body, text, 13, weight=600, color=C.green, bg=fill).pack()

        RoundedButton(self.body, S.VIEW_BOOK, lambda: on_open(book), variant="outline",
                      icon="book-open-1", icon_size=17, expand=True).pack(fill="x", pady=(11, 0))


class CatalogView(tk.Frame):
    def __init__(self, master, model, controller):
        super().__init__(master, bg=C.page)
        self.model = model
        self.controller = controller
        self._page_buttons = {}
        self._cards = {}

        content = tk.Frame(self, bg=C.page)
        content.pack(fill="x", padx=32, pady=32)
        self._build_header(content)
        self._build_filters(content)
        self._build_summary(content)
        self._grid = tk.Frame(content, bg=C.page)
        self._grid.pack(fill="x", pady=(0, 20))
        for i in range(4):
            self._grid.columnconfigure(i, weight=1, uniform="book")
        self._build_pagination(content)
        self._build_banner(content)
        self.activity = ActivityView(content, model, controller)
        self.activity.pack(fill="x", padx=32, pady=(28, 24))
        self.refresh()

    def _build_header(self, content):
        head = tk.Frame(content, bg=C.page)
        head.pack(fill="x", pady=(0, 20))
        TextBlock(head, S.CATALOG_TITLE, 32, color=C.ink, mode="fill", lh=1.35,
                  bg=C.page).pack(fill="x")
        TextBlock(head, S.CATALOG_GREETING, 16, color=C.muted, mode="fill", lh=1.35,
                  bg=C.page).pack(fill="x", pady=(6, 0))

    def _build_filters(self, content):
        row = tk.Frame(content, bg=C.page)
        row.pack(fill="x", pady=(0, 20))
        SearchField(row, S.SEARCH_PLACEHOLDER, self.controller.search_changed).pack(
            side="left", fill="x", expand=True)
        SelectBox(row, S.GRADE_OPTIONS, S.GRADE_ALL, self.controller.grade_changed,
                  width=208).pack(side="left", padx=(14, 0))
        SelectBox(row, S.CATEGORY_OPTIONS, S.CATEGORY_ALL, self.controller.category_changed,
                  width=240).pack(side="left", padx=(14, 0))

    def _build_summary(self, content):
        row = tk.Frame(content, bg=C.page)
        row.pack(fill="x", pady=(0, 20))
        left = tk.Frame(row, bg=C.page)
        left.pack(side="left")
        TextBlock(left, S.AVAILABLE_SUMMARY, 16, weight=600, color=C.ink, bg=C.page).pack(side="left")
        TextBlock(left, S.ALL_HAVE_ACTIVITY, 14, color=C.muted, bg=C.page).pack(side="left", padx=(12, 0))
        right = tk.Frame(row, bg=C.page)
        right.pack(side="right")
        TextBlock(right, S.SORT_LABEL, 14, color=C.muted, bg=C.page).pack(side="left")
        tk.Label(right, image=assets.icon("chevron-down", 16), bg=C.page, bd=0).pack(
            side="left", padx=(7, 0))

    def _build_pagination(self, content):
        row = tk.Frame(content, bg=C.page)
        row.pack(fill="x", pady=(0, 20))
        TextBlock(row, S.PAGINATION_TEXT, 14, color=C.muted, bg=C.page).pack(side="left")
        buttons = tk.Frame(row, bg=C.page)
        buttons.pack(side="right")
        RoundedButton(buttons, S.PREV_PAGE,
                      lambda: self.controller.go_to_page(self.model.page - 1),
                      variant="ghost").pack(side="left")
        for number in range(1, self.model.total_pages + 1):
            btn = RoundedButton(buttons, str(number),
                                lambda n=number: self.controller.go_to_page(n),
                                variant="outline")
            btn.pack(side="left", padx=(7, 0))
            self._page_buttons[number] = btn
        RoundedButton(buttons, S.NEXT_PAGE,
                      lambda: self.controller.go_to_page(self.model.page + 1),
                      variant="outline").pack(side="left", padx=(7, 0))

    def _build_banner(self, content):
        banner = Surface(content, fill=C.sage, radius=10, pad=(22, 22, 22, 22))
        banner.pack(fill="x", pady=(0, 20))
        tk.Label(banner.body, image=assets.icon("messages-square", 30), bg=C.sage, bd=0).pack(side="left")
        text_col = tk.Frame(banner.body, bg=C.sage)
        text_col.pack(side="left", fill="x", expand=True, padx=(20, 20))
        TextBlock(text_col, S.BANNER_TITLE, 21, weight=600, color=C.ink, mode="fill",
                  lh=1.35, bg=C.sage).pack(fill="x")
        TextBlock(text_col, S.BANNER_TEXT, 15, color=C.green, mode="fill", lh=1.35,
                  bg=C.sage).pack(fill="x", pady=(4, 0))
        TextBlock(banner.body, S.BANNER_STEPS, 15, weight=600, color=C.ink, lh=1.35,
                  bg=C.sage).pack(side="right")

    def refresh(self):
        """Muestra solo las tarjetas de la página actual. Las tarjetas se crean una vez
        y se reutilizan, así no se destruyen ni se vuelven a dibujar al hacer clic."""
        books = self.model.page_books()[:4]
        visible_ids = {book["id"] for book in books}
        for book_id, card in self._cards.items():
            if book_id not in visible_ids:
                card.grid_remove()
        for index, book in enumerate(books):
            card = self._cards.get(book["id"])
            if card is None:
                card = BookCard(self._grid, book, self.controller.open_book)
                self._cards[book["id"]] = card
            card.grid(row=0, column=index, sticky="nsew",
                      padx=(0 if index == 0 else 10, 0 if index == 3 else 10))
        for number, btn in self._page_buttons.items():
            btn.set_variant("solid" if number == self.model.page else "outline")
