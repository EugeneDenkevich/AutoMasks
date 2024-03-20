from dataclasses import dataclass
from app.utils.misc import get_result_path


@dataclass
class Settings:
    API_URL: str = "https://cvat2.trainingdata.solutions/api"
    RESULT_PATH: str = get_result_path()
    TRANSPARENCY: int = 100


settings = Settings()
