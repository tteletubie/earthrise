from models.app_model import AppModel


class AppController:
    def __init__(self, model: AppModel | None = None) -> None:
        self._model = model or AppModel()

    def test_interface(self) -> dict[str, str]:
        self._model.test_interface()
        return {"message": self._model.message}

    def get_status(self) -> dict[str, str]:
        return {"message": self._model.message}
