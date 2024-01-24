import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    API_URL = os.getenv("API_URL")
    USERNAME = os.getenv("USER-NAME")
    PASSWORD = os.getenv("PASS-WORD")
    RESULT_PATH = (
        Path(__file__).resolve().parent.parent.parent / "result"
    ).resolve()


settings = Settings()
