from tkinter import messagebox


class MenuController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_button_command("jugar", self.on_play)
        self.view.set_button_command("opciones", self.on_options)
        self.view.set_button_command("otros", self.on_others)

    def on_play(self):
        messagebox.showinfo("Jugar", "Aquí irá la sección de juegos.")

    def on_options(self):
        messagebox.showinfo("Opciones", "Aquí irán las opciones.")

    def on_others(self):
        messagebox.showinfo("Otros", "Aquí irá la sección de otros.")
