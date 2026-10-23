import os
import tkinter as tk

from dotenv import load_dotenv

from models.menu_model import MenuModel
from views.menu_view import MenuView
from controllers.menu_controller import MenuController

load_dotenv()


def main():
    app_title = os.getenv("APP_TITLE", "Biblioteca Primaria")

    root = tk.Tk()
    root.title(app_title)
    root.geometry("600x500")
    root.minsize(480, 400)
    root.configure(bg="#FFF8E7")

    model = MenuModel(app_title)
    view = MenuView(root, model.get_title(), model.get_options())
    MenuController(model, view)

    root.mainloop()


if __name__ == "__main__":
    main()
