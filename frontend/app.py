import flet as ft

from frontend import settings


def main_app(page: ft.Page):
    page.title = settings.TITLE
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 350
    page.window_height = 500
    page.window_resizable = False

    txt_id_list = ft.TextField(width=150)
    choise_instance = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(label="jobs", value="jobs"),
                ft.Radio(label="tasks", value="tasks"),
            ]
        )
    )

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Выберите:"),
                        choise_instance,
                        ft.Text("id (через запятую):"),
                        txt_id_list,
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
