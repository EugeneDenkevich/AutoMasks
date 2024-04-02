from pathlib import Path
from contextlib import contextmanager
import sqlite3
from app.backend.src.settings import settings


class DBsqlite:
    """Класс базы данных sqlite"""

    def __init__(self) -> None:
        # self.con = sqlite3.connect(settings.DB_PATH)
        # self.cur = self.con.cursor()
        self.db_init()

    # @contextmanager
    # def connection(self):
    #     connection = sqlite3.connect(settings.DB_PATH)
    #     try:
    #         yield connection
    #     finally:
    #         connection.close()

    def db_init(self) -> None:
        with sqlite3.Connection(settings.DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS  credentials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login VARCHAR(254),
                    password VARCHAR(254)
                );
                """
            )
            if not cursor.execute("SELECT id FROM credentials;").fetchone():
                cursor.execute(
                    """
                    INSERT INTO credentials (id, login, password) VALUES (1, "", "");
                    """
                )
            connection.commit()

    def get_login(self) -> str | None:
        with sqlite3.Connection(settings.DB_PATH) as connection:
            cursor = connection.cursor()
            login = cursor.execute("SELECT login FROM credentials;").fetchone()[0]
            return login

    def get_password(self) -> str | None:
        with sqlite3.Connection(settings.DB_PATH) as connection:
            cursor = connection.cursor()
            password = cursor.execute("SELECT password FROM credentials;").fetchone()[0]
            return password

    def set_login(self, new_login: str) -> None:
        with sqlite3.Connection(settings.DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE credentials SET login=? WHERE id=1;", (new_login,))
            connection.commit()

    def set_password(self, new_password: str) -> None:
        with sqlite3.Connection(settings.DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE credentials SET password=? WHERE id=1;", (new_password,))
            connection.commit()
    
    def save_credentials(self, username, password) -> None:
        self.set_login(username)
        self.set_password(password)


db_sqlite = DBsqlite()
