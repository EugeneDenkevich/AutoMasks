import os
from dataclasses import dataclass
from typing import final

from backend.src.settings import settings


@final
@dataclass
class MainService:
    """Класс для всгпомогательных операций"""

    over: bool = False

    def cancel(self):
        """Останавливаем обработку данных"""
        self.over = True

    def clean(self):
        """Возобновляем обработку данных"""
        self.over = False

    def create_result_path(self):
        """Создаём папку \"results\" """
        if not settings.RESULT_PATH.exists():
            os.mkdir(settings.RESULT_PATH)


main_service = MainService()
