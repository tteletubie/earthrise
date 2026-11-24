(function () {
    function closeProfileDialog(app) {
        const profileDialog = app.querySelector(".registro-del-maestro");
        profileDialog?.remove();
        document.body.style.overflow = "";
    }

    function bindRoute(app, navigate, selector, route) {
        app.querySelectorAll(selector).forEach((element) => {
            const activate = () => navigate(route);
            element.addEventListener("click", activate);
            element.addEventListener("keydown", (event) => {
                if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                activate();
                }
            });
        });
    }

    function initialize(app, navigate) {
        bindRoute(app, navigate, ".botn:not(a)", "#book");
        bindRoute(app, navigate, ".icono-maestro:not(.cap-home)", "#admin");
        bindRoute(app, navigate, ".cap-home", "#home");

        app.querySelectorAll("[data-route]").forEach((element) => {
            element.addEventListener("click", () => navigate(element.dataset.route));
        });

        const profileDialog = app.querySelector(".registro-del-maestro");
        profileDialog?.querySelector(".cancelar")?.addEventListener("click", () => {
            closeProfileDialog(app);
        });
        profileDialog?.addEventListener("click", (event) => {
            if (event.target === profileDialog) {
            closeProfileDialog(app);
            }
        });

        const saveProfileButton = profileDialog?.querySelector(
            ".guardar-y-continuar",
        );
        saveProfileButton?.addEventListener("click", async () => {
            const nombre = profileDialog
            .querySelector('[name="nombre"]')
            ?.value.trim();
            const apellido = profileDialog
            .querySelector('[name="apellido"]')
            ?.value.trim();
            const idGrado = Number(
            profileDialog.querySelector('[name="grado"]')?.value,
            );

            if (!nombre || !apellido || !idGrado) {
            return;
            }

            saveProfileButton.disabled = true;
            const activeResult = await window.api.usuario.getActive();
            const payload = {
            nombre,
            apellido_paterno: apellido,
            id_grado: idGrado,
            };

            if (activeResult.success && activeResult.data?.id_usuario) {
            payload.id_usuario = activeResult.data.id_usuario;
            }

            const result = await window.api.usuario.create(payload);
            saveProfileButton.disabled = false;

            if (!result.success) {
            console.error(result.error);
            return;
            }

            closeProfileDialog(app);
            navigate("#home");
        });

        const escapeHandler = (event) => {
            if (event.key === "Escape") {
            closeProfileDialog(app);
            }
        };
        if (window.homeEscapeHandler) {
            document.removeEventListener("keydown", window.homeEscapeHandler);
        }
        window.homeEscapeHandler = escapeHandler;
        document.addEventListener("keydown", escapeHandler);
    }

    window.HomeController = { initialize };
})();
