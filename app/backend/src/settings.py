from dataclasses import dataclass
from pathlib import Path
import os
import sys


@dataclass
class Settings:
    API_URL = "https://cvat2.trainingdata.solutions/api"
    # RESULT_PATH = Path(__file__).resolve() / "result"
    # RESULT_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
    RESULT_PATH = Path(sys.argv[0]).parent
    TRANSPARENCY: int = 100


settings = Settings()
