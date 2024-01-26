import os
from xml.etree import ElementTree as ET

from src.masks import drow_masks
from src.queries import get_data
from src.utils import _get_colors
from src.utils import extract_zip
from src.utils import filter_images


def process_instance(_id, _type, _format, transparency, type_element):
    """
    Download and drow masks on all images in the job.
    """
    transparency = int(2.55 * transparency)
    images_zip, annotations_zip = get_data(_type, _id, _format)
    image_path = extract_zip(_id, images_zip, is_image=True)
    annotations_path = extract_zip(_id, annotations_zip)

    file_xml = annotations_path / "annotations.xml"

    tree = ET.parse(file_xml)
    root = tree.getroot()

    labels = root.findall(f"./meta/{_type[0:-1]}/labels//label")
    colors = _get_colors(labels)
    images = root.findall(".//image")
    images_filtered = filter_images(images, type_element)

    drow_masks(images_filtered, colors, _id, transparency, type_element)

    if file_xml.exists():
        os.remove(file_xml)
