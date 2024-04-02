class RetryExceprion(Exception):
    """Исключение при неудачной попытке скачивания архива"""


class NotZipFile(Exception):
    """Исключение при неудачной попытке распаковки архива"""


class ImageNotFoundError(Exception):
    """Исключение при неудачной попытке создания экземпляра изображения"""


class EmptyIdListError(Exception):
    """Исключение при отправке пустого списка id"""


class ProcessWasStopped(Exception):
    """Исключение при нажатии на кнопку \"Отмена\" """


class InvalidIdError(Exception):
    """Исключение при некорректных id"""


class CantCreateFolderError(Exception):
    """Исключение при попытке создать папку"""


class ImageNotFoundServerError(Exception):
    """Исключение при отсутствии озображений на сервере"""


class TaskNotFoundError(Exception):
    """Исключение при отсутствии указанной таски"""


class NotAuthorizedError(Exception):
    """Исключение при неверном логине и пароле"""

class ClientConnectionError(Exception):
    """Исключение при плохом соединении"""
