class MenuModel:
    def __init__(self, title):
        self.title = title
        self.options = [
            ("jugar", "Jugar"),
            ("opciones", "Opciones"),
            ("otros", "Otros"),
        ]

    def get_title(self):
        return self.title

    def get_options(self):
        return list(self.options)
