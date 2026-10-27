# GATITO500 · Entre páginas (tkinter)

Réplica en Python + tkinter del diseño HTML/CSS "Entre páginas · Banco de libros escolar".

## Requisitos
- Python 3.9 o superior (con tkinter; viene incluido en Windows y macOS oficiales)
- Pillow: `pip install -r requirements.txt`

## Ejecutar
```
python main.py
```

- La ventana abre a una proporción de la pantalla (no a 1280x960).
- **F11**: pantalla completa real, sin barra de título. El diseño se adapta al tamaño, no se estira.
- **Esc**: sale de pantalla completa.

## Estructura (MVC)
```
main.py                     arranque
config/                     tema (colores, fuentes), textos, ajustes
models/library_model.py     MODELO: libros, preguntas, filtros y paginación
views/                      VISTA
  widgets.py                componentes personalizados (Canvas): cajas redondeadas,
                            botones, textos con interlineado CSS, campos, scroll
  sidebar.py, catalog_view.py, activity_view.py, main_window.py
controllers/app_controller.py  CONTROLADOR: eventos y actualización de la vista
assets/images/              ilustraciones de las portadas
assets/icons/               SVG originales y PNG (4x) usados como iconos
assets/fonts/               Source Sans 3 (Regular, Bold y SemiBold)
tools/build_icons.py        regenera los PNG si cambias los SVG
```

## Notas
- Las fuentes incluidas se cargan solo en Windows. En macOS/Linux instala
  "Source Sans 3" en el sistema para ver la tipografía exacta; si no, tkinter usa una alternativa.
- Los iconos `<img>` del HTML que no tenían `src` (sliders, escuela de la sección de cierre,
  biblioteca de la sección de consejo y el icono de la primera pregunta) se conservan como
  espacio vacío, igual que en el navegador. Para mostrarlos, agrégalos a `assets/icons`.
- Para agregar libros 5 a 10, añádelos a `BOOKS` en `models/library_model.py`.
- Los gatillos de acción (abrir libro, finalizar actividad, cerrar sesión) están vacíos en
  `controllers/app_controller.py`, igual que el script del HTML.
