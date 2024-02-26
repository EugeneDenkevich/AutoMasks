from app.backend.src.drower import Drawer
from app.backend.src.exceptions import CantCreateFolderError
from app.backend.src.exceptions import ProcessWasStopped
from app.backend.src.job import Job
from app.utils.main_service import main_service


def handle_job(id: int):
    """Обработка сущности job"""

    # Готовим данные:
    job = Job(id)
    try:
        job.create_path()
    except Exception:
        raise CantCreateFolderError()
    annotations_xml = job.download_annotations()
    images = job.get_images()

    # Создаём экземплар рисовальщика:
    drawer = Drawer(annotations_xml)
    drawer.get_data()

    # Обрабатываем изображения:
    for image in images:
        if main_service.over is False:
            job.download_image(image)
            drawer.draw_mask(image)
        else:
            raise ProcessWasStopped()


def handle_task(task_id: int):
    """Обработка сущности task"""
    raise NotImplementedError()


def handle_project(project_id: int):
    """Обработка сущности project"""
    raise NotImplementedError()
