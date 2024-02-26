from pydantic import BaseModel

from app.backend.src.enums import TypeEnum


class InputDTO(BaseModel):
    """DTO модель для введённый пользователем данных"""

    username: str
    password: str
    id_list: list[int]
    type: TypeEnum
    transparency: int
