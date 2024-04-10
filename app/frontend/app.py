from traceback import format_exc

import flet as ft

from app.backend.main import main as backend_main
from app.backend.src.exceptions import CantCreateFolderError
from app.backend.src.exceptions import EmptyIdListError
from app.backend.src.exceptions import ImageNotFoundServerError
from app.backend.src.exceptions import InvalidIdError
from app.backend.src.exceptions import NotZipFile
from app.backend.src.exceptions import ProcessWasStopped
from app.backend.src.exceptions import RetryExceprion
from app.backend.src.exceptions import ImageNotFoundError
from app.backend.src.exceptions import TaskNotFoundError
from app.backend.src.exceptions import NotAuthorizedError
from app.backend.src.exceptions import ClientConnectionError
from app.backend.src.settings import settings
from app.frontend.radio import type_radio_group
from app.utils.main_service import main_service
from app.utils.misc import open_depends_os
from app.backend.src.gateways.db import db_sqlite


login_value = db_sqlite.get_login()
password_value = db_sqlite.get_password()


def main_app(page: ft.Page):
    page.title = "AutoMask"
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 470
    page.window_height = 760
    page.bgcolor = ft.colors.INDIGO_100

    btn_size = 110

    username_text = ft.TextField(label="Логин", width=300, value=login_value)
    username = ft.Row([username_text], alignment=ft.MainAxisAlignment.CENTER)
    password_text = ft.TextField(
        label="Пароль", width=300, value=password_value, can_reveal_password=True, password=True,
    )
    password = ft.Row([password_text], alignment=ft.MainAxisAlignment.CENTER)
    list_id_text = ft.TextField(
        label="id (через пробел):", width=300, height=50
    )
    list_id = ft.Row([list_id_text], alignment=ft.MainAxisAlignment.CENTER)
    help_text = ft.Text(visible=False, color=ft.colors.GREEN)
    txt_error = ft.Text(
        color=ft.colors.RED,
        width=250,
    )
    error_presentation = ft.Column(
        [
            txt_error,
        ],
        width=300,
        scroll=ft.ScrollMode.ALWAYS,
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def open_folder(e):
        open_depends_os(settings.RESULT_PATH)

    def show_help_text(_type: str) -> None:
        if _type == "canceled":
            help_text.value = "Отмена операции, подождите..."
            help_text.color = ft.colors.RED
        elif _type == "ready":
            help_text.value = "Готово"
            help_text.color = ft.colors.GREEN
        elif _type == "empty":
            help_text.value = "Заполните все пустые поля"
            help_text.color = ft.colors.RED
        help_text.visible = True
        page.update()

    def hide_help_text() -> None:
        help_text.visible = False
        page.update()
        
    def hide_error():
        error_presentation.visible = False
        page.update()

    def cancel(e):
        hide_error()
        if main_service.processing is False:
            return
        show_help_text("canceled")
        main_service.cancel()

    def show_error(message: str):
        progress_bar.visible = False
        txt_error.value = message
        error_presentation.height = 100 if len(txt_error.value) > 60 else None
        error_presentation.visible = True
        hide_help_text()
        page.update()

    def init_start():
        main_service.start()
        help_text.visible = False
        hide_error()
        page.update()

    def shutdown_start():
        if error_presentation.visible is True:
            error_presentation.visible = False
        progress_bar.visible = False
        folder_button.disabled = False
        page.update()

    def start(e):
        if username_text.value == "":
            show_help_text("empty")
            return
        if password_text.value == "":
            show_help_text("empty")
            return
        init_start()
        try:
            progress_bar.value = 0
            progress_bar.visible = True
            page.update()
            backend_main(
                username=username_text.value,
                password=password_text.value,
                id_list=list_id_text.value,
                type=type_radio_group.value,
                transparency=str(slider.value),
                progress_bar=progress_bar,
            )
        except NotAuthorizedError:
            show_error("Неверные логин и пароль")
            return
        except RetryExceprion:
            show_error("Нет связи с сервером CVAT")
            return
        except NotZipFile:
            show_error("Проблема распаковки zip-архива")
            return
        except ImageNotFoundError:
            show_error("Не найдены необходимые изображения")
            return
        except EmptyIdListError:
            show_error("Вы не указали ни одного id")
            return
        except ProcessWasStopped:
            show_error("Операция отменена")
            return
        except InvalidIdError:
            show_error("Введите корректные id через пробел")
            return
        except NotImplementedError:
            show_error("Функционал ещё не реализован")
            return
        except CantCreateFolderError as err:
            show_error("Ошибка при создании папки \"result\"")
            return
        except ImageNotFoundServerError:
            show_error("Не найдены изображения на сервере CVAT.")
            return
        except TaskNotFoundError:
            show_error("Таски не найдены.")
            return
        except ClientConnectionError:
            show_error("Проверьте соединение с интернетом.")
            return
        except Exception:
            show_error(format_exc())
            raise Exception()
        finally:
            main_service.stop()
        shutdown_start()
        show_help_text("ready")

    slider_label = ft.Text(value=50, size=18)
    start_button = ft.ElevatedButton("Старт", width=btn_size, on_click=start)
    cancel_button = ft.ElevatedButton(
        "Отмена", width=btn_size, on_click=cancel
    )
    folder_button = ft.ElevatedButton(
        "Папка",
        width=btn_size,
        disabled=False,
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
                            username,
                            password,
                            ft.Column(
                                [
                                    ft.Text("Выберите:"),
                                    type_radio_group,
                                ],
                            ),
                            list_id,
                            error_presentation,
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
