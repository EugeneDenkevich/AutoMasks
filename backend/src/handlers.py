import os
import shutil
from zipfile import ZipFile

from backend.src.schemas import InputDTO
from backend.src.settings import settings
from backend.src.queries import get_archives
from backend.src.utils import extract_archives


def handle_job(job_id: int):
    """Обработка сущности job"""       

    # Cоздаём директорию для job.
    instance_path = settings.RESULT_PATH / str(job_id)
    if instance_path.exists():
        shutil.rmtree(instance_path)

    # Получаем и извлекаем архивы.
    extract_archives(instance_path, **get_archives(job_id))
    rename_images()
    # Продолжение следует...
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    rename_images(image_path, annotations_path)

    file_xml = annotations_path / "annotations.xml"

    tree = ET.parse(file_xml)
    root = tree.getroot()

    labels = root.findall(f"./meta/job/labels//label")
    colors = _get_colors(labels)

    images = root.findall(".//image")

    drow_masks(images, colors, _id, settings.TRANSPARENCY)

    if file_xml.exists():
        os.remove(file_xml)

def handle_task(input: InputDTO):
    """Обработка сущности task"""
    pass


def handle_project(input: InputDTO):
    """Обработка сущности project"""
    pass