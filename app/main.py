"""
Приложение для нанесения масок на изображения.

Для тестов:

jobs:
1234 47268

tasks:
4436 4434

projects:
214
"""
import logging

import flet as ft
from frontend.app import main_app

logging.basicConfig(level=logging.INFO)

ft.app(
    target=main_app,
)
