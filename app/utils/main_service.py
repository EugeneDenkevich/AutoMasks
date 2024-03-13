import os
from dataclasses import dataclass
from typing import final

from app.backend.src.settings import settings


@final
@dataclass
class MainService:
    """Класс для всгпомогательных операций"""

    over: bool = False
    processing: bool = False

    def cancel(self):
        """Останавливаем обработку данных"""
        self.over = True

    def start(self):
        """Возобновляем обработку данных"""
        self.over = False
        self.processing = True

    def stop(self):
        """Останавливаем обработку данных"""
        self.processing = False

    def create_result_path(self):
        """Создаём папку \"results\" """
        if not settings.RESULT_PATH.exists():
            os.mkdir(settings.RESULT_PATH)


main_service = MainService()
