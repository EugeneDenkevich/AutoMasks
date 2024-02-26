import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    API_URL = "https://cvat2.trainingdata.solutions/api"
    RESULT_PATH = Path(".").resolve() / "result"
    TRANSPARENCY: int = 100


settings = Settings()
