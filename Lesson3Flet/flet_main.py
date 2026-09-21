import flet as ft

RIDDLES = [
    ("Белый, но не сахар. Пушистый, но не птица. Нет ног, а идёт.", "снег"),
    ("Страус может назвать себя птицей?", "нет"),
    ("Каких камней не бывает в речке?", "сухих"),
    ("Что можно увидеть с закрытыми глазами?", "сон"),
    ("Висит груша — нельзя скушать. Что это?", "лампочка"),
]

PASS_SCORE = 3


def main(page: ft.Page):
    page.title = "Викторина: загадки"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 30
    page.window.width = 520
    page.window.height = 620

    state = {"name": "", "index": 0, "score": 0}

    def show_start():
        page.clean()
        name_field = ft.TextField(
            label="Как тебя зовут?",
            width=300,
            autofocus=True,
            on_submit=lambda e: start_game(name_field.value),
        )
        page.add(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Викторина: загадки", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        f"Ответь верно хотя бы на {PASS_SCORE} из {len(RIDDLES)} загадок.",
                        size=14,
                        color=ft.Colors.GREY_700,
                    ),
                    name_field,
                    ft.Button(
                        content="Начать",
                        icon=ft.Icons.PLAY_ARROW,
                        on_click=lambda e: start_game(name_field.value),
                    ),
                ],
            )
        )

    def start_game(name):
        state["name"] = name.strip() or "Игрок"
        state["index"] = 0
        state["score"] = 0
        show_question()

    def show_question():
        page.clean()
        i = state["index"]
        question, correct = RIDDLES[i]

        answer_field = ft.TextField(
            label="Твой ответ",
            width=300,
            autofocus=True,
            on_submit=lambda e: submit_answer(answer_field, correct),
        )
        feedback = ft.Text("", size=14)

        page.add(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=18,
                controls=[
                    ft.Text(f"Загадка {i + 1} из {len(RIDDLES)}", size=14, color=ft.Colors.GREY_700),
                    ft.ProgressBar(value=i / len(RIDDLES), width=300),
                    ft.Container(
                        content=ft.Text(question, size=18, text_align=ft.TextAlign.CENTER),
                        padding=20,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        width=340,
                    ),
                    answer_field,
                    feedback,
                    ft.Button(
                        content="Ответить",
                        icon=ft.Icons.CHECK,
                        on_click=lambda e: submit_answer(answer_field, correct),
                    ),
                    ft.Text(f"Счёт: {state['score']}", size=13, color=ft.Colors.GREY_600),
                ],
            )
        )

    def submit_answer(answer_field, correct):
        if answer_field.value.lower().strip() == correct:
            state["score"] += 1
        state["index"] += 1
        if state["index"] < len(RIDDLES):
            show_question()
        else:
            show_result()

    def show_result():
        page.clean()
        score = state["score"]
        won = score >= PASS_SCORE
        if won:
            verdict = f"Поздравляю, {state['name']}! Ты выиграл!"
            color = ft.Colors.GREEN
        else:
            verdict = f"Увы, {state['name']}. Попробуй ещё раз!"
            color = ft.Colors.RED

        page.add(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Результат", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Верных ответов: {score} из {len(RIDDLES)}", size=18),
                    ft.Text(verdict, size=18, color=color, text_align=ft.TextAlign.CENTER),
                    ft.Button(
                        content="Играть заново",
                        icon=ft.Icons.REPLAY,
                        on_click=lambda e: show_start(),
                    ),
                ],
            )
        )

    show_start()


ft.run(main)
ft.run(main, view=ft.AppView.WEB_BROWSER)
