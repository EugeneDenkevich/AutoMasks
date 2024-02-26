from backend.src.enums import TypeEnum
from pydantic import BaseModel


class InputDTO(BaseModel):
    """DTO модель для введённый пользователем данных"""

    username: str
    password: str
    id_list: list[int]
    type: TypeEnum
    transparency: int
