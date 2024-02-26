import requests


def get_session():
    with requests.Session() as session:
        return session


session = get_session()
