from dataclasses import dataclass
from app.utils.misc import create_result_path


@dataclass
class Settings:
    API_URL: str = "https://cvat2.trainingdata.solutions/api"
    RESULT_PATH: str = create_result_path()
    TRANSPARENCY: int = 100


settings = Settings()
