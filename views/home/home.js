import {
    BookOpen,
    ChevronDown,
    Library,
    LogOut,
    MessagesSquare,
    School,
    Search,
    createIcons,
} from "../../node_modules/lucide/dist/esm/lucide.mjs";

const testButton = document.querySelector("#test-btn");
const message = document.querySelector("#message");

createIcons({
    icons: {
        BookOpen,
        ChevronDown,
        Library,
        LogOut,
        MessagesSquare,
        School,
        Search,
    },
});

function waitForApi() {
    if (window.pywebview?.api) {
        return Promise.resolve(window.pywebview.api);
    }

    return new Promise((resolve) => {
        window.addEventListener(
            "pywebviewready",
            () => resolve(window.pywebview.api),
            { once: true },
        );
    });
}

if (testButton && message) {
    testButton.addEventListener("click", async () => {
        const api = await waitForApi();
        const result = await api.test_interface();
        message.textContent = result.message;
    });
}
