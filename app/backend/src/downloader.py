from typing import List
import os

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from zipfile import ZipFile
from zipfile import BadZipFile

from app.backend.src.exceptions import NotZipFile
from app.backend.src.exceptions import RetryExceprion
from app.backend.src.exceptions import NotAuthorizedError
from app.backend.src.session import session
from app.backend.src.settings import settings
from app.backend.src.enums import TypeEnum


class Downloader:

    @retry(
        stop=stop_after_attempt(300),
        retry=retry_if_exception_type(RetryExceprion),
    )
    def get_images(self, objects: list[int], obj_type: TypeEnum) -> List[Element]:
        """
        Скачивание аннотаций из списка id-шников сущностей.
        Получение всех изображений из этого списка.
        
        :param objects: Список id-шников сущностей.
        :param obj_type: Тип сущности (jobs, tasks, projects).
        :return: Все изображения сущностей.
        """
        images_total = []
        for id_ in objects:
            response = session.get(
                url=f"{settings.API_URL}/{obj_type.value}/{id_}/annotations",
                params={
                    "action": "download",
                    "format": "CVAT for images 1.1",
                },
            )
            if response.status_code == 401:
                raise NotAuthorizedError()
            annotations = response.content
            if not annotations:
                raise RetryExceprion()
            path_zip = settings.RESULT_PATH / "annotations.zip"
            with open(path_zip, "wb") as f:
                f.write(annotations)
            try:
                with ZipFile(path_zip, "r") as f:
                    f.extractall(settings.RESULT_PATH)
            except BadZipFile as e:
                raise NotZipFile(e)
            tree = ET.parse(settings.RESULT_PATH / "annotations.xml")
            images = tree.getroot().findall(".//image")
            if path_zip.exists():
                os.remove(path_zip)
            annotations_xml = settings.RESULT_PATH / "annotations.xml"
            if annotations_xml.exists():
                os.remove(annotations_xml)
            images_total.extend(images)
        return images_total


downloader = Downloader()
