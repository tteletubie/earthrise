import ArrowLeft from "../../node_modules/lucide/dist/esm/icons/arrow-left.mjs";
import Clock3 from "../../node_modules/lucide/dist/esm/icons/clock-3.mjs";
import Eye from "../../node_modules/lucide/dist/esm/icons/eye.mjs";
import EyeOff from "../../node_modules/lucide/dist/esm/icons/eye-off.mjs";
import MessagesSquare from "../../node_modules/lucide/dist/esm/icons/messages-square.mjs";
import Projector from "../../node_modules/lucide/dist/esm/icons/projector.mjs";
import SlidersHorizontal from "../../node_modules/lucide/dist/esm/icons/sliders-horizontal.mjs";
import Sprout from "../../node_modules/lucide/dist/esm/icons/sprout.mjs";
import createElement from "../../node_modules/lucide/dist/esm/createElement.mjs";

const icons = {
    "arrow-left": ArrowLeft,
    "clock-3": Clock3,
    eye: Eye,
    "eye-off": EyeOff,
    "messages-square": MessagesSquare,
    projector: Projector,
    "sliders-horizontal": SlidersHorizontal,
    sprout: Sprout,
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
