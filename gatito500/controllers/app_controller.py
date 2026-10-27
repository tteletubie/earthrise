"""CONTROLADOR: recibe los eventos de la vista, cambia el modelo y pide a la vista refrescarse."""
from models.library_model import LibraryModel
from views.main_window import MainWindow


class AppController:
    def __init__(self, root):
        self.root = root
        self.model = LibraryModel()
        self._fullscreen = False
        self.view = MainWindow(root, self.model, self)
        self.view.catalog.refresh()
        root.bind("<F11>", self.toggle_fullscreen)
        root.bind("<Escape>", self.exit_fullscreen)

    # ---- Catálogo ----
    def search_changed(self, text):
        self.model.search_text = text
        self.model.page = 1
        self.view.catalog.refresh()

    def grade_changed(self, value):
        self.model.grade = value
        self.model.page = 1
        self.view.catalog.refresh()

    def category_changed(self, value):
        self.model.category = value
        self.model.page = 1
        self.view.catalog.refresh()

    def go_to_page(self, page):
        self.model.page = max(1, min(page, self.model.total_pages))
        self.view.catalog.refresh()

    def open_book(self, book):
        """Gancho: aquí va la acción al abrir un libro (en el HTML el handler estaba vacío)."""
        pass

    # ---- Actividad ----
    def toggle_answer(self, qid):
        self.model.toggle_answer(qid)
        self.view.activity.refresh()

    def hide_all_answers(self):
        self.model.hide_all_answers()
        self.view.activity.refresh()

    def finish_activity(self):
        """Gancho: acción de 'Finalizar actividad'."""
        pass

    # ---- Sesión ----
    def logout(self):
        """Gancho: acción de 'Cerrar sesión'."""
        pass

    # ---- Pantalla completa ----
    def toggle_fullscreen(self, _event=None):
        self._set_fullscreen(not self._fullscreen)

    def exit_fullscreen(self, _event=None):
        self._set_fullscreen(False)

    def _set_fullscreen(self, on):
        self._fullscreen = on
        self.root.attributes("-fullscreen", on)
