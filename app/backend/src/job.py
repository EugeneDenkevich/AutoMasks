from httpx import ReadTimeout
from typing import final
import os
import shutil
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import BadZipFile
from zipfile import ZipFile
from io import BytesIO

from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from PIL import Image

from app.backend.src.exceptions import NotZipFile
from app.backend.src.exceptions import RetryExceprion
from app.backend.src.exceptions import ImageNotFoundServerError
from app.backend.src.exceptions import NotAuthorizedError
from app.backend.src.exceptions import ClientConnectionError
from app.backend.src.session import session
from app.backend.src.settings import settings


@final
class Job:
    """Класс сущности job"""

    job_path: Path = None

    def __init__(self, job_id, image=None):
        self.job_id = job_id
        self.image = image

    def create_path(self, **kwargs):
        """Создание директории для job"""
        if "different_path" in kwargs:
            self.job_path = kwargs["different_path"] / str(self.job_id)
        else:
            self.job_path = settings.RESULT_PATH / str(self.job_id)
        if self.job_path.exists():
            shutil.rmtree(self.job_path)
        os.mkdir(self.job_path)

    @retry(
        stop=stop_after_attempt(30),
        retry=retry_if_exception_type(RetryExceprion),
    )
    def download_annotations(self) -> Path:
        """
        Скачать аннотации сущности job
        :return: Путь к аннотациями
        """
        response = session.get(
            url=f"{settings.API_URL}/jobs/{self.job_id}/annotations",
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
        path_zip = self.job_path / "annotations.zip"
        with open(path_zip, "wb") as f:
            f.write(annotations)
        try:
            with ZipFile(path_zip, "r") as f:
                f.extractall(self.job_path)
        except BadZipFile as e:
            raise NotZipFile(e)
        if path_zip.exists():
            os.remove(path_zip)
        return self.job_path / "annotations.xml"

    @retry(
        stop=stop_after_attempt(30),
        retry=retry_if_exception_type(RetryExceprion),
    )
    def download_image(self, image: dict):
        """Скачать изображение"""
        for frame, image_name in image.items():
            try:
                image_response = session.get(
                    url=f"{settings.API_URL}/jobs/{self.job_id}/data",
                    params={
                        "type": "frame",
                        "number": frame,
                    },
                )
            except ReadTimeout:
                raise ClientConnectionError()
            if image_response.status_code == 401:
                raise NotAuthorizedError()
            if image_response.status_code == 500:
                raise ImageNotFoundServerError()
            img_path = self.job_path / image_name
            with open(img_path, "wb") as f:
                file = BytesIO(image_response.content)
                img = Image.open(file)
                img.save(self.job_path / image_name)

    @retry(
        stop=stop_after_attempt(30),
        retry=retry_if_exception_type(RetryExceprion),
    )
    def get_images(self) -> list[dict]:
        """Получение словаря с id и именами изображений сущности job"""
        tree = ET.parse(self.job_path / "annotations.xml")
        start_frame = int(tree.getroot().find("./meta/job/start_frame").text)
        stop_frame = int(tree.getroot().find("./meta/job/stop_frame").text)
        frames = range(start_frame, stop_frame + 1)
        images = tree.getroot().findall(".//image")
        result_images = []
        for image, frame in zip(images, frames):
            result_images.append(
                {frame: image.attrib.get("name").split("/")[-1]}
            )
        return result_images

    @property
    def path(self):
        return self.job_path
