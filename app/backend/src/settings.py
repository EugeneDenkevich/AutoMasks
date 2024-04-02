from pathlib import Path
from dataclasses import dataclass
from app.utils.misc import get_result_path
from app.utils.misc import get_db_path


@dataclass
class Settings:
    API_URL: str = "https://cvat2.trainingdata.solutions/api"
    RESULT_PATH: Path = get_result_path()
    DB_PATH: Path = get_db_path()
    TRANSPARENCY: int = 100


settings = Settings()
