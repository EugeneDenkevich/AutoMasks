from backend.src.drower import Drawer
from backend.src.exceptions import ProcessWasStopped
from backend.src.job import Job
from utils.main_service import main_service


def handle_job(id: int):
    """Обработка сущности job"""

    # Готовим данные:
    job = Job(id)
    job.create_path()
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
    pass


def handle_project(project_id: int):
    """Обработка сущности project"""
    pass
