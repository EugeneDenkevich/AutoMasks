import logging

from dotenv import load_dotenv


def load_config():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
