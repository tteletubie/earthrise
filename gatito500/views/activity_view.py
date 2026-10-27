"""VISTA: actividad (preguntas) y guía del maestro con respuestas que se muestran u ocultan."""
import tkinter as tk

from config import strings as S
from config.theme import C, font
from views.widgets import RoundedButton, Spacer, Surface, TextBlock


class ActivityView(tk.Frame):
    def __init__(self, master, model, controller):
        super().__init__(master, bg=C.page)
        self.model = model
        self.controller = controller
        self._answer_boxes = {}
        self._toggle_buttons = {}
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=320)

        left = tk.Frame(self, bg=C.page)
        left.grid(row=0, column=0, sticky="nsew")
        right = tk.Frame(self, bg=C.page)
        right.grid(row=0, column=1, sticky="nsew", padx=(24, 0))
        self._build_left(left)
        self._build_right(right)
        self.refresh()

    def _build_left(self, parent):
        act = self.model.activity
        head = tk.Frame(parent, bg=C.page)
        head.pack(fill="x")
        TextBlock(head, act["eyebrow"], 14, weight=600, color=C.green, mode="fill",
                  lh=1.35, bg=C.page).pack(fill="x")
        TextBlock(head, act["title"], 36, color=C.ink, mode="fill", lh=1.35,
                  bg=C.page).pack(fill="x", pady=(8, 0))
        TextBlock(head, act["intro"], 18, color=C.muted, mode="fill", lh=1.35,
                  bg=C.page).pack(fill="x", pady=(8, 0))

        questions = tk.Frame(parent, bg=C.page)
        questions.pack(fill="x", pady=(20, 0))
        for question in self.model.questions:
            self._build_question(questions, question)

        closing = tk.Frame(parent, bg=C.page)
        closing.pack(fill="x", padx=5, pady=(5, 0))
        Spacer(closing, 22, 22, C.page).pack(side="left")
        TextBlock(closing, act["closing"], 17, color=C.green, mode="fill", lh=1.35,
                  bg=C.page).pack(side="left", fill="x", expand=True, padx=(10, 0))

    def _build_question(self, parent, question):
        card = Surface(parent, fill=C.surface, border=C.border, radius=10, pad=(22, 22, 22, 22))
        card.pack(fill="x", pady=(0, 20))
        row = card.body

        number = Surface(row, fill=C.sage, radius=6, width=38, height=38)
        number.pack(side="left", anchor="n", padx=(0, 18))
        tk.Label(number.body, text=str(question["id"]), font=font(22, 600), fg=C.ink,
                 bg=C.sage, bd=0).pack(expand=True)

        content = tk.Frame(row, bg=C.surface)
        content.pack(side="left", fill="x", expand=True)
        TextBlock(content, question["tag"], 13, weight=600, color=C.muted, bg=C.surface).pack(anchor="w")
        TextBlock(content, question["text"], 25, weight=600, color=C.ink, mode="fill",
                  lh=1.25, bg=C.surface).pack(fill="x", pady=(10, 0))

        if question["answer"] is not None:
            box = Surface(content, fill=C.sage, radius=6, pad=(16, 16, 16, 16))
            TextBlock(box.body, S.ANSWER_LABEL, 13, weight=600, color=C.green,
                      bg=C.sage).pack(anchor="w")
            TextBlock(box.body, question["answer"], 21, color=C.ink, mode="fill", lh=1.35,
                      bg=C.sage).pack(fill="x", pady=(5, 0))
            self._answer_boxes[question["id"]] = box

    def _build_right(self, parent):
        act = self.model.activity

        support = Surface(parent, fill=C.surface, border=C.border, radius=10, pad=(22, 22, 22, 22))
        support.pack(fill="x")
        sb = support.body
        head = tk.Frame(sb, bg=C.surface)
        head.pack(fill="x")
        Spacer(head, 21, 21, C.surface).pack(side="left")
        TextBlock(head, act["guide_title"], 21, weight=600, color=C.ink,
                  bg=C.surface).pack(side="left", padx=(9, 0))
        TextBlock(sb, act["guide_text"], 15, color=C.muted, mode="fill", lh=1.35,
                  bg=C.surface).pack(fill="x", pady=(20, 0))

        for question in self.model.questions:
            qid = question["id"]
            group = tk.Frame(sb, bg=C.surface)
            group.pack(fill="x", pady=(20, 0))
            state = tk.Frame(group, bg=C.surface)
            state.pack(fill="x")
            TextBlock(state, f'Pregunta {qid} · {question["guide_label"]}', 15, weight=600,
                      color=C.ink, bg=C.surface).pack(side="left")
            if qid == 1:  # en el HTML la primera pregunta tenía un icono sin src a la derecha
                Spacer(state, 17, 17, C.surface).pack(side="right")
            btn = RoundedButton(group, S.HIDE_ANSWER, lambda q=qid: self.controller.toggle_answer(q),
                                variant="outline", blank_icon=True, expand=True)
            btn.pack(fill="x", pady=(8, 0))
            self._toggle_buttons[qid] = btn

        RoundedButton(sb, S.HIDE_ALL_ANSWERS, self.controller.hide_all_answers,
                      variant="ghost", weight=400, expand=True).pack(fill="x", pady=(20, 0))

        tip = Surface(parent, fill=C.cream, radius=10, pad=(22, 22, 22, 22))
        tip.pack(fill="x", pady=(20, 0))
        tb = tip.body
        time_row = tk.Frame(tb, bg=C.cream)
        time_row.pack(fill="x")
        Spacer(time_row, 20, 20, C.cream).pack(side="left")
        TextBlock(time_row, act["tip_time"], 16, weight=600, color=C.ink,
                  bg=C.cream).pack(side="left", padx=(8, 0))
        TextBlock(tb, act["tip_title"], 16, weight=600, color=C.ink, mode="fill",
                  bg=C.cream).pack(fill="x", pady=(12, 0))
        TextBlock(tb, act["tip_text"], 15, color=C.green, mode="fill", lh=1.5,
                  bg=C.cream).pack(fill="x", pady=(12, 0))

        RoundedButton(parent, S.FINISH_ACTIVITY, self.controller.finish_activity,
                      variant="solid", height=42, blank_icon=True,
                      expand=True).pack(fill="x", pady=(20, 0))

    def refresh(self):
        """Muestra u oculta cada respuesta según el modelo y actualiza los botones."""
        for question in self.model.questions:
            qid = question["id"]
            visible = self.model.answer_visible[qid]
            box = self._answer_boxes.get(qid)
            if box is not None:
                if visible:
                    box.pack(fill="x", pady=(10, 0))
                else:
                    box.pack_forget()
            btn = self._toggle_buttons.get(qid)
            if btn is not None:
                btn.set_text(S.HIDE_ANSWER if visible else S.SHOW_ANSWER)
