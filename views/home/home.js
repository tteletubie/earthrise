const testButton = document.querySelector("#test-btn");
const message = document.querySelector("#message");

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
