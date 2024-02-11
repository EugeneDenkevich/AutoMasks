import os
import shutil
from xml.etree import ElementTree as ET
import logging

from backend.src.masks import drow_masks
from backend.src.queries import get_jobs_data
from backend.src.settings import settings
from backend.src.utils import _get_colors
from backend.src.utils import extract_zip
from backend.src.utils import rename_images


def process_instance(_id, _format, transparency):
    """
    Download and drow masks on all images in the job.
    """

    instance_path = settings.RESULT_PATH / str(_id)
    if instance_path.exists():
        shutil.rmtree(instance_path)
    transparency = int(2.55 * transparency)
    jobs_data = get_jobs_data(_id, _format)
    if isinstance(jobs_data, int):
        raise Exception(f"Downloading status_code: {jobs_data}")
    images_zip, annotations_zip = jobs_data
    image_path = extract_zip(_id, images_zip, is_image=True)
    annotations_path = extract_zip(_id, annotations_zip)

    rename_images(image_path, annotations_path)

    file_xml = annotations_path / "annotations.xml"

    tree = ET.parse(file_xml)
    root = tree.getroot()

    labels = root.findall(f"./meta/job/labels//label")
    colors = _get_colors(labels)

    images = root.findall(".//image")

    drow_masks(images, colors, _id, transparency)

    if file_xml.exists():
        os.remove(file_xml)
