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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # isort: ignore
sys.path.append(str(ROOT))  # isort: ignore

import flet as ft

from app.config import load_config
from app.frontend.app import main_app

load_config()

ft.app(
    target=main_app,
    name="AutoMask",
)
