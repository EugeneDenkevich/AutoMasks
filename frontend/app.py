import os
from pathlib import Path
from time import sleep

import flet as ft

from backend.main import main as backend_main
from frontend import settings


def main_app(page: ft.Page):
    page.title = settings.TITLE
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 390
    page.window_height = 560
    page.window_resizable = False
    page.bgcolor = ft.colors.INDIGO_100

    txt_id_list = ft.TextField(width=300, height=50)
    jobs_radio = ft.Radio(label="jobs", value="jobs")
    tasks_radio = ft.Radio(label="tasks", value="tasks")
    choise_instance = ft.RadioGroup(
        value="jobs",
        content=ft.Row(
            [
                jobs_radio,
                tasks_radio,
            ]
        ),
    )

    def open_folder(e):
        folder_path = Path(__file__).parent.parent / "result"

        if not folder_path.exists():
            os.mkdir(folder_path)
        os.startfile(folder_path)

    slider_label = ft.Text(value=50)
    folder_button = ft.ElevatedButton(
        "Папка", width=120, disabled=True, on_click=open_folder
    )
    progress_bar = ft.ProgressBar(
        width=300, color=ft.colors.BLUE_600, bgcolor="#eeeeee", visible=False
    )

    def slider_change(e):
        slider_label.value = int(e.control.value)
        page.update()

    def start(e):
        """
        fixme:

        Сделать прогрессбар по такому шаблону:

            async def button_clicked(e):
            t.value = "Doing something..."
            await t.update_async()
            b.disabled = True
            await b.update_async()
            for i in range(0, 101):
                pb.value = i * 0.01
                await asyncio.sleep(0.1)
                await pb.update_async()
            t.value = "Click the button..."
            await t.update_async()
            b.disabled = False
            await b.update_async()

        Но не асинхронно.
        """
        # backend_main(
        #     id_list=...,
        #     _type=...,
        #     transparency=...,
        # )
        progress_bar.visible = True
        page.update()
        sleep(4)
        progress_bar.visible = False
        folder_button.disabled = False
        page.update()

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                ft.Text(
                                    " • Заполните все поля и нажмите 'Старт'.\n"
                                    " • Дождитесь окончания загрузки\n"
                                    " • Затем нажмите 'Папка'\n"
                                    " • При вводе некорректых данных\n"
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
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Старт", width=120, on_click=start
                                    ),
                                    folder_button,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                width=300,
                            ),
                            progress_bar,
                        ],
                    ),
                    bgcolor=ft.colors.GREY_100,
                    padding=15,
                    border_radius=20,
                    # height=700,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )
