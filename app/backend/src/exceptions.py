class RetryExceprion(Exception):
    """Исключение при неудачной попытке скачивания архива"""


class NotZipFile(Exception):
    """Исключение при неудачной попытке распаковки архива"""


class ImageNotFound(Exception):
    """Исключение при неудачной попытке создания экземпляра изображения"""


class EmptyIdListError(Exception):
    """Исключение при отправке пустого списка id"""


class ProcessWasStopped(Exception):
    """Исключение при нажатии на кнопку \"Отмена\" """


class InvalidIdError(Exception):
    """Исключение при некорректных id"""
