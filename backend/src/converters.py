from backend.src.schemas import InputDTO


def row_data_to_dto(
    username: str,
    password: str,
    id_list: str,
    type: str,
    format: str,
    transparency: str,
) -> InputDTO:
    return InputDTO(
        username=username,
        password=password,
        id_list=list(map(lambda n: int(n.strip()), id_list.split())),
        type=type,
        format=format,
        transparency=int(2.55*transparency)
    )
