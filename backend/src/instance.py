import os
import shutil
from xml.etree import ElementTree as ET

from backend.src.masks import drow_masks
from backend.src.queries import get_data
from backend.src.settings import settings
from backend.src.utils import _get_colors
from backend.src.utils import extract_zip
from backend.src.utils import filter_images
from backend.src.utils import rename_images


def process_instance(_id, _type, _format, transparency, type_element):
    """
    Download and drow masks on all images in the job.
    """

    # 1. Скачиваем файлы:
    # - изображения (все в рамках джобы/таска/проекта);
    # - аннотации (1 файл, относящийся к джобе/таску/проекту).
    #
    # 2. Разархивируем файлы в папку "result" в корне проекта.

    instance_path = settings.RESULT_PATH / str(_id)
    if instance_path.exists():
        shutil.rmtree(instance_path)
    transparency = int(2.55 * transparency)
    images_zip, annotations_zip = get_data(_type, _id, _format)
    image_path = extract_zip(_id, images_zip, is_image=True)
    annotations_path = extract_zip(_id, annotations_zip)

    # ------------

    # Переименовать изображения согласно оригинала

    rename_images(image_path, annotations_path)

    # ------------

    # Получаем все цвета в файле "annotations.xml".

    file_xml = annotations_path / "annotations.xml"

    tree = ET.parse(file_xml)
    root = tree.getroot()

    labels = root.findall(f"./meta/{_type[0:-1]}/labels//label")
    colors = _get_colors(labels)

    # ------------

    # Собираем все image в файле "annotations.xml".

    images = root.findall(".//image")
    # images_filtered = filter_images(images, type_element)

    # ------------

    # Рисуем маски на всех изображениях в папке results.

    drow_masks(images, colors, _id, transparency)

    # ------------

    # Удаляем лишнее:
    # - файл "annotations.xml"

    if file_xml.exists():
        os.remove(file_xml)

    # ------------
