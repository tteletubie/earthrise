import customtkinter as ctk

from views.home_view import HomeView


def main():
    root = ctk.CTk()
    root.title("Biblioteca del maestro")
    root.geometry("1440x960")
    root.minsize(1080, 720)
    root.resizable(True, True)
    HomeView(root).pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
