import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class MainView(ttk.Frame):
    def __init__(self, master: tk.Misc, on_test: Callable[[], None]) -> None:
        super().__init__(master, padding=16)
        self._build(on_test)

    def _build(self, on_test: Callable[[], None]) -> None:
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Basic MCP with Tkinter", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, pady=(0, 12), sticky="w")
        ttk.Label(self, text="Basic application organized with MVC.").grid(row=1, column=0, pady=(0, 12), sticky="w")

        self.message = tk.StringVar(value="Ready to use.")
        ttk.Label(self, textvariable=self.message).grid(row=2, column=0, pady=(0, 12), sticky="w")

        ttk.Button(self, text="Test", command=on_test).grid(row=3, column=0, sticky="w")

    def show_message(self, message: str) -> None:
        self.message.set(message)
