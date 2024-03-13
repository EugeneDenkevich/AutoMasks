from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    API_URL = "https://cvat2.trainingdata.solutions/api"
    RESULT_PATH = Path(__file__).resolve() / "result"
    TRANSPARENCY: int = 100


settings = Settings()
