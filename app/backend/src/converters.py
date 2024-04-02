from app.backend.src.exceptions import EmptyIdListError
from app.backend.src.exceptions import InvalidIdError
from app.backend.src.schemas import InputDTO


def row_data_to_dto(
    username: str,
    password: str,
    id_list: str,
    type: str,
    transparency: str,
) -> InputDTO:
    if id_list == "":
        raise EmptyIdListError()
    try:
        finished_id_list = list(map(lambda n: int(n.strip()), id_list.split()))
    except ValueError as err:
        raise InvalidIdError(err)
    return InputDTO(
        username=username,
        password=password,
        id_list=finished_id_list,
        type=type,
        transparency=int(2.55 * int(float(transparency))),
    )
