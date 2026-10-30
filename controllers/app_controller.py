import tkinter as tk

from models.app_model import AppModel
from views.main_view import MainView


class AppController:
    def __init__(self, model: AppModel | None = None) -> None:
        self.model = model or AppModel()
        self.window = tk.Tk()
        self.window.title("Basic MCP")
        self.window.minsize(420, 180)
        self.view = MainView(self.window, self.test_interface)
        self.view.pack(fill="both", expand=True)

    def test_interface(self) -> None:
        self.model.test_interface()
        self.view.show_message(self.model.message)

    def run(self) -> None:
        self.window.mainloop()
