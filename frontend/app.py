import os
import sys
import webbrowser as wb
from pathlib import Path
from traceback import format_exc
import logging

sys.path.append(str(Path(__file__).parent.parent))

import flet as ft
from dotenv import load_dotenv

from backend.main import main as backend_main
from frontend import settings
from utils.main_process import main_process
from utils.misc import open_depends_os

load_dotenv()

login_value = os.environ.get("USER-NAME", "")
password_value = os.environ.get("PASS-WORD", "")


def main_app(page: ft.Page):
    page.title = settings.TITLE
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 390
    page.window_height = 660
    page.bgcolor = ft.colors.INDIGO_100

    btn_size = 110
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
    login_text = ft.TextField(label="Логин", width=300, value=login_value)
    login = ft.Row([login_text], alignment=ft.MainAxisAlignment.CENTER)
    password_text = ft.TextField(
        label="Пароль", width=300, value=password_value
    )
    password = ft.Row([password_text], alignment=ft.MainAxisAlignment.CENTER)
    list_id_text = ft.TextField(
        label="id (через пробел или запятую):", width=300, height=50
    )
    list_id = ft.Row([list_id_text], alignment=ft.MainAxisAlignment.CENTER)
    help_text = ft.Text(value="Готово.", visible=False, color=ft.colors.GREEN)

    def open_folder(e):
        folder_path = (Path.cwd() / "result").resolve()

        if not folder_path.exists():
            os.mkdir(folder_path)
        open_depends_os(str(folder_path))

    def show_help_text(_type: str) -> None:
        if _type == "canceled":
            help_text.value = "Отменено"
            help_text.color = ft.colors.RED
        elif _type == "ready":
            help_text.value = "Готово"
            help_text.color = ft.colors.GREEN
        help_text.visible = True

    def start(e):
        main_process.over = False
        help_text.visible = False
        page.update()
        id_list = get_id_list(list_id_text.value)
        if login_text.value == "":
            pass
        if password_text.value == "":
            pass
        if id_list == -1:
            txt_error.value = (
                "Пожалуйста, введите корректные id через пробел или запятую."
            )
            if txt_error.visible == False:
                txt_error.visible = True
                page.update()
            return
        else:
            if txt_error.visible == True:
                txt_error.visible = False
                page.update()
        progress_bar.visible = True
        page.update()
        try:
            backend_main(
                id_list=id_list,
                _type=choise_instance.value,
                transparency=slider.value,
                login=login_text.value,
                password=password_text.value,
            )
        except Exception as e:
            progress_bar.visible = False
            txt_error.value = format_exc()
            txt_error.visible = True
            logging.error(f"{e}")
            page.update()
            return
        if txt_error.visible == True:
            txt_error.visible = False
        progress_bar.visible = False
        folder_button.disabled = False
        show_help_text("Готово")
        page.update()

    def cancel(e):
        main_process.over = True
        show_help_text("Отмена операции, подождите...")

    slider_label = ft.Text(value=50, size=18)
    start_button = ft.ElevatedButton("Старт", width=btn_size, on_click=start)
    cancel_button = ft.ElevatedButton(
        "Отмена", width=btn_size, on_click=cancel
    )
    folder_button = ft.ElevatedButton(
        "Папка",
        width=btn_size,
        disabled=True,
        on_click=open_folder,
    )
    progress_bar = ft.ProgressBar(
        width=250, color=ft.colors.BLUE_600, bgcolor="#eeeeee", visible=False
    )

    def slider_change(e):
        slider_label.value = int(e.control.value)
        page.update()

    slider = ft.Slider(
        value=50,
        min=0,
        max=100,
        on_change=slider_change,
        width=350,
        divisions=10,
    )
    txt_error = ft.Text(
        visible=False,
        color=ft.colors.RED,
        width=250,
    )

    def get_id_list(txt_id_list):
        try:
            id_list = list(map(int, txt_id_list.split()))
            return id_list
        except:
            pass
        try:
            id_list = list(map(int, txt_id_list.split(",")))
            return id_list
        except Exception as e:
            return -1

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
                            login,
                            password,
                            ft.Column(
                                [
                                    ft.Text("Выберите:"),
                                    choise_instance,
                                ],
                            ),
                            list_id,
                            txt_error,
                            ft.Text("Прозрачность маски:"),
                            ft.Row(
                                [slider_label],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Stack(
                                [
                                    ft.Row(
                                        [slider],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text(
                                                        "Прозрачная", size=13
                                                    ),
                                                    ft.Text(
                                                        "Не прозрачная",
                                                        size=13,
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                width=320,
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ],
                                height=60,
                            ),
                            ft.Row(
                                [
                                    ft.Row(
                                        [
                                            start_button,
                                            cancel_button,
                                            folder_button,
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        width=340,
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [progress_bar],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [help_text],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    bgcolor=ft.colors.GREY_100,
                    padding=15,
                    width=370,
                    border_radius=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

# if __name__ == "__main__":
    # ft.app(
    #     target=main_app,
    # )
