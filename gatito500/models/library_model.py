"""MODELO: datos de la biblioteca, de la actividad y estado de filtros/paginación.
Aquí se agregan los libros 5 a 10 cuando los tengas (el HTML solo trae 4)."""
import math

from config import strings as S
from config.settings import BOOKS_PER_PAGE, TOTAL_CATALOG_BOOKS

TEACHER = {"initials": "MG", "name": "María García", "role": "Maestro · 2.º A"}

BOOKS = [
    {"id": 1, "title": "La semilla de Luna", "author": "Elena Ríos", "minutes": 10,
     "grade": "2.º grado", "category": "Naturaleza",
     "cover_bg": "#e6ede3", "image": "cuento_luna.png"},
    {"id": 2, "title": "El viaje de una gota", "author": "Pablo Montes", "minutes": 8,
     "grade": "2.º grado", "category": "Ciencia",
     "cover_bg": "#e5edef", "image": "cuento_gota.png"},
    {"id": 3, "title": "Un abrazo para erizo", "author": "Lucía Vidal", "minutes": 7,
     "grade": "1.º grado", "category": "Convivencia",
     "cover_bg": "#f5e8e0", "image": "cuento_erizo.png"},
    {"id": 4, "title": "El cielo de Tomás", "author": "Inés Navarro", "minutes": 12,
     "grade": "3.º grado", "category": "Imaginación",
     "cover_bg": "#f5ebd4", "image": "cuento_cielo.png"},
]

ACTIVITY = {
    "eyebrow": "LA SEMILLA DE LUNA · PARA CONVERSAR EN GRUPO",
    "title": "Una semilla, muchas manos",
    "intro": "Escuchen cada pregunta, compartan sus ideas y construyan una respuesta juntos.",
    "closing": "Todas las ideas cuentan. Recuerden explicar el porqué de su respuesta.",
    "guide_title": "Guía del maestro",
    "guide_text": ("Muestra cada respuesta después de escuchar al grupo. "
                   "Las preguntas 2 y 3 siguen sin respuesta visible."),
    "tip_time": "8 minutos · 2.º grado",
    "tip_title": "Dales tiempo para pensar",
    "tip_text": ("Invita a participar a distintas voces. En la última pregunta, "
                 "acuerden una acción de cuidado para el salón."),
}

QUESTIONS = [
    {"id": 1, "guide_label": "Recordar", "tag": "RECORDAR",
     "text": "¿Qué necesitaba la semilla para crecer?",
     "answer": "Agua, luz, tiempo y cuidados."},
    {"id": 2, "guide_label": "Comprender", "tag": "COMPRENDER",
     "text": "¿Por qué Luna y sus amigos se turnaron para cuidar la planta?",
     "answer": None},
    {"id": 3, "guide_label": "Conectar", "tag": "CONECTAR CON NUESTRA ESCUELA",
     "text": "¿Qué podríamos cuidar juntos en nuestra escuela?",
     "answer": None},
]


class LibraryModel:
    def __init__(self):
        self.teacher = TEACHER
        self.books = BOOKS
        self.activity = ACTIVITY
        self.questions = [dict(q) for q in QUESTIONS]
        self.answer_visible = {q["id"]: q["answer"] is not None for q in self.questions}
        self.search_text = ""
        self.grade = S.GRADE_ALL
        self.category = S.CATEGORY_ALL
        self.page = 1

    @property
    def total_pages(self):
        return math.ceil(TOTAL_CATALOG_BOOKS / BOOKS_PER_PAGE)

    def filtered_books(self):
        text = self.search_text.strip().lower()
        result = []
        for book in self.books:
            if self.grade != S.GRADE_ALL and book["grade"] != self.grade:
                continue
            if self.category != S.CATEGORY_ALL and book["category"] != self.category:
                continue
            haystack = f'{book["title"]} {book["author"]} {book["category"]}'.lower()
            if text and text not in haystack:
                continue
            result.append(book)
        return result

    def page_books(self):
        start = (self.page - 1) * BOOKS_PER_PAGE
        return self.filtered_books()[start:start + BOOKS_PER_PAGE]

    def get_question(self, qid):
        return next((q for q in self.questions if q["id"] == qid), None)

    def toggle_answer(self, qid):
        question = self.get_question(qid)
        if question is None or question["answer"] is None:
            return  # sin respuesta en el HTML: no hace nada
        self.answer_visible[qid] = not self.answer_visible[qid]

    def hide_all_answers(self):
        for qid in self.answer_visible:
            self.answer_visible[qid] = False
