import os
from pathlib import Path
from types import NoneType
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from backend.src.settings import settings


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


def _get_coords(element, type_element):
    coords = []
    if type_element == "polygon":
        row_coords = element.attrib.get("points").split(";")
        for coord in row_coords:
            x = float(coord.split(",")[0])
            y = float(coord.split(",")[1])
            coords.append((x, y))
    elif type_element == "box":
        xtl = float(element.attrib.get("xtl"))
        ytl = float(element.attrib.get("ytl"))
        xbr = float(element.attrib.get("xbr"))
        ybr = float(element.attrib.get("ybr"))
        coords.extend([xtl, ytl, xbr, ybr])
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


def sort_by_zorder(elements: "list[ET.Element]") -> "list[ET.Element]":
    if len(elements) == 0:
        return []
    z_orders = []
    for element in elements:
        z_order = element.attrib.get("z_order")
        z_orders.append(z_order)
    sorted_z_order = sorted(set(z_orders), key=int)
    result: "list[ET.Element]" = []
    for order in sorted_z_order:
        for element in elements:
            if element.attrib.get("z_order") == order:
                result.append(element)
    return result


def filter_images(images, type_element) -> list[ET.Element]:
    """
    Get only annotated images
    """
    image_list = []
    for image in images:
        polygon = image.find(f"./{type_element}")
        if not isinstance(polygon, NoneType):
            image_list.append(image)
    return image_list
