import os
from pathlib import Path

os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu --disable-gpu-compositing")
import webview
from controllers.app_controller import AppController


def main() -> None:
    controller = AppController()
    home_path = (Path(__file__).parent / "views" / "home" / "home.html").resolve()
    webview.create_window(
        "Basic MCP",
        url=home_path.as_uri(),
        js_api=controller,
        #width=480,
        #height=260,
        #min_size=(420, 180),
        resizable=True,
    )
    webview.start()


if __name__ == "__main__":
    main()
