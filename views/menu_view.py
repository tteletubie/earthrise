import tkinter as tk

BACKGROUND = "#FFF8E7"
TITLE_COLOR = "#264653"

BUTTON_STYLES = {
    "jugar": ("#2A9D8F", "white"),
    "opciones": ("#E9C46A", TITLE_COLOR),
    "otros": ("#E76F51", "white"),
}


class MenuView(tk.Frame):
    def __init__(self, master, title, options):
        super().__init__(master, bg=BACKGROUND)
        self.pack(fill="both", expand=True)
        self.buttons = {}

        center = tk.Frame(self, bg=BACKGROUND)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center,
            text=title,
            font=("Helvetica", 28, "bold"),
            fg=TITLE_COLOR,
            bg=BACKGROUND,
        ).pack(pady=(0, 30))

        for key, label in options:
            bg, fg = BUTTON_STYLES.get(key, ("#8ECAE6", TITLE_COLOR))
            button = tk.Button(
                center,
                text=label,
                width=18,
                font=("Helvetica", 16, "bold"),
                bg=bg,
                fg=fg,
                activebackground=TITLE_COLOR,
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                pady=10,
            )
            button.pack(pady=8)
            self.buttons[key] = button

    def set_button_command(self, key, command):
        self.buttons[key].config(command=command)
