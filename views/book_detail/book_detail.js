import ArrowLeft from "../../node_modules/lucide/dist/esm/icons/arrow-left.mjs";
import ArrowRight from "../../node_modules/lucide/dist/esm/icons/arrow-right.mjs";
import BookOpen from "../../node_modules/lucide/dist/esm/icons/book-open.mjs";
import Clock3 from "../../node_modules/lucide/dist/esm/icons/clock-3.mjs";
import Lightbulb from "../../node_modules/lucide/dist/esm/icons/lightbulb.mjs";
import Library from "../../node_modules/lucide/dist/esm/icons/library.mjs";
import LogOut from "../../node_modules/lucide/dist/esm/icons/log-out.mjs";
import MessagesSquare from "../../node_modules/lucide/dist/esm/icons/messages-square.mjs";
import Monitor from "../../node_modules/lucide/dist/esm/icons/monitor.mjs";
import Projector from "../../node_modules/lucide/dist/esm/icons/projector.mjs";
import School from "../../node_modules/lucide/dist/esm/icons/school.mjs";
import createElement from "../../node_modules/lucide/dist/esm/createElement.mjs";

const icons = {
    "arrow-left": ArrowLeft,
    "arrow-right": ArrowRight,
    "book-open": BookOpen,
    "clock-3": Clock3,
    lightbulb: Lightbulb,
    library: Library,
    "log-out": LogOut,
    "messages-square": MessagesSquare,
    monitor: Monitor,
    projector: Projector,
    school: School,
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

const homeUrl = "../home/home.html";

document.querySelector("#opcinDeNavegacin")?.addEventListener("click", () => {
    window.location.href = homeUrl;
});

document.querySelector("#volverAlCatlogo")?.addEventListener("click", () => {
    window.location.href = homeUrl;
});
