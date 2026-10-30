import BookOpen from "../../node_modules/lucide/dist/esm/icons/book-open.mjs";
import ChevronDown from "../../node_modules/lucide/dist/esm/icons/chevron-down.mjs";
import Library from "../../node_modules/lucide/dist/esm/icons/library.mjs";
import LogOut from "../../node_modules/lucide/dist/esm/icons/log-out.mjs";
import MessagesSquare from "../../node_modules/lucide/dist/esm/icons/messages-square.mjs";
import School from "../../node_modules/lucide/dist/esm/icons/school.mjs";
import Search from "../../node_modules/lucide/dist/esm/icons/search.mjs";
import createElement from "../../node_modules/lucide/dist/esm/createElement.mjs";

const icons = {
    "book-open": BookOpen,
    "chevron-down": ChevronDown,
    library: Library,
    "log-out": LogOut,
    "messages-square": MessagesSquare,
    school: School,
    search: Search,
};

document.querySelectorAll("[data-lucide]").forEach((iconElement) => {
    const iconName = iconElement.dataset.lucide;
    const iconNode = icons[iconName];

    if (!iconNode) {
        return;
    }

    const svgElement = createElement(iconNode, {
        ...Object.fromEntries(
            Array.from(iconElement.attributes).map((attribute) => [
                attribute.name,
                attribute.value,
            ]),
        ),
        class: `lucide lucide-${iconName} ${iconElement.className}`,
    });

    iconElement.replaceWith(svgElement);
});

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
