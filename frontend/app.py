import flet as ft

from frontend import settings


def main_app(page: ft.Page):
    page.title = settings.TITLE
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 500
    page.window_resizable = False

    txt_id_list = ft.TextField(width=300, height=50)
    choise_instance = ft.RadioGroup(
        value="jobs",
        content=ft.Row(
            [
                ft.Radio(label="jobs", value="jobs"),
                ft.Radio(label="tasks", value="tasks"),
            ]
        ),
    )

    slider_label = ft.Text(value=50)

    def slider_change(e):
        slider_label.value = int(e.control.value)
        page.update()

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Container(
                            ft.Text(
                                "Заполните все поля и нажмите 'Старт'.\n"
                                "Затем нажмите 'Папка'\n"
                                "При вводе некорректых данных\n"
                                "программа подскажет, что нужно исправить.",
                            ),
                            bgcolor=ft.colors.GREY_300,
                            padding=10,
                            border_radius=10,
                        ),
                        ft.Column(
                            [
                                ft.Text("Выберите:"),
                                choise_instance,
                            ]
                        ),
                        ft.Text("id (через запятую):"),
                        txt_id_list,
                        ft.Text("Прозрачность маски:"),
                        slider_label,
                        ft.Stack(
                            [
                                ft.Slider(
                                    value=50,
                                    min=0,
                                    max=100,
                                    on_change=slider_change,
                                    width=300,
                                    divisions=10,
                                ),
                                ft.Row(
                                    [
                                        ft.Text("Прозрачная", size=13),
                                        ft.Text("Не прозрачная", size=13),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    width=300,
                                ),
                            ],
                            height=60,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            width=350,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
