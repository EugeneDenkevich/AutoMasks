import os
from pathlib import Path
from types import NoneType
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from src.settings import settings


def extract_zip(job, archive, is_image: bool = False) -> Path:
    """
    Extract zip-archive and get path to folder called like instance's id
    """
    path = (settings.RESULT_PATH / str(job)).resolve()
    if not path.exists():
        os.makedirs(path)
    path_zip = (path / f"{job}.zip").resolve()
    with open(path_zip, "wb") as f:
        f.write(archive)
    with ZipFile(path_zip, "r") as f:
        f.extractall(path)
        if is_image:
            images = f.filelist
            for image in images:
                image_name = image.filename.split(".")[0]
                format = image.filename.split(".")[1]
                os.rename(
                    path / image.filename,
                    path / f"{str(int(image_name))}.{format}",
                )
    if path_zip.exists():
        os.remove(path_zip)
    return path


def hex_to_rgb(hex_color):
    only_numbers = hex_color.lstrip("#")
    rgb_color_code = [int(only_numbers[i : i + 2], 16) for i in (0, 2, 4)]
    return rgb_color_code


def _get_coords(polygon):
    coords = []
    row_coords = polygon.attrib.get("points").split(";")
    for coord in row_coords:
        x = float(coord.split(",")[0])
        y = float(coord.split(",")[1])
        coords.append((x, y))
    return coords


def _get_colors(labels) -> dict:
    """
    Get labels and their codes of colors
    """
    colors = {}
    for label in labels:
        name = label.find("./name").text
        color = label.find("./color").text
        colors[name] = color
    return colors


def sort_by_zorder(polygons: "list[ET.Element]") -> "list[ET.Element]":
    z_orders = []
    for polygon in polygons:
        z_order = polygon.attrib.get("z_order")
        z_orders.append(z_order)
    sorted_z_order = sorted(set(z_orders), key=int)
    result: "list[ET.Element]" = []
    for order in sorted_z_order:
        for polygon in polygons:
            if polygon.attrib.get("z_order") == order:
                result.append(polygon)
    return result


def filter_images(images) -> list[ET.Element]:
    """
    Get only annotated images
    """
    image_list = []
    for image in images:
        polygon = image.find("./polygon")
        if not isinstance(polygon, NoneType):
            image_list.append(image)
    return image_list
