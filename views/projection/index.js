import ArrowLeft from "../../node_modules/lucide/dist/esm/icons/arrow-left.mjs";
import ArrowRight from "../../node_modules/lucide/dist/esm/icons/arrow-right.mjs";
import BookOpen from "../../node_modules/lucide/dist/esm/icons/book-open.mjs";
import Minimize2 from "../../node_modules/lucide/dist/esm/icons/minimize-2.mjs";
import createElement from "../../node_modules/lucide/dist/esm/createElement.mjs";

const icons = {
    "arrow-left": ArrowLeft,
    "arrow-right": ArrowRight,
    "book-open": BookOpen,
    "minimize-2": Minimize2,
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


document.querySelectorAll("#ir_actividad").forEach((bookButton) => {
    bookButton.addEventListener("click", () => {
        window.location.href = "../teacher_guide/index.html";
    });
});
