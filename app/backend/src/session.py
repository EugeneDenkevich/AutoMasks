import httpx


def get_session():
    session = httpx.Client()
    return session


session = get_session()
