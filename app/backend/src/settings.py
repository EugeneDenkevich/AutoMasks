from pathlib import Path
from dataclasses import dataclass
from app.utils.misc import get_result_path
from app.utils.misc import get_db_path
from app.utils.misc import get_log_path
import logging
from dotenv import load_dotenv


@dataclass
class Settings:
    API_URL: str = "https://cvat2.trainingdata.solutions/api"
    RESULT_PATH: Path = get_result_path()
    DB_PATH: Path = get_db_path()
    LOG_PATH: Path = get_log_path()
    TRANSPARENCY: int = 100
    
    def set_logs(self):
        logging.basicConfig(
        level=logging.INFO,
        filename=settings.LOG_PATH,
        format="%(asctime)s %(levelname)s %(message)s",
)


settings = Settings()
settings.set_logs()
load_dotenv()
