from app.backend.src.drower import Drawer
from app.backend.src.exceptions import CantCreateFolderError
from app.backend.src.exceptions import ProcessWasStopped
from app.backend.src.job import Job
from app.backend.src.task import Task
from app.utils.main_service import main_service


def handle_job(job_id: int, **kwargs):
    """Обработка сущности job"""

    # Готовим данные:
    job = Job(job_id)
    try:
        job.create_path(**kwargs)
    except Exception:
        raise CantCreateFolderError()
    annotations_xml = job.download_annotations()
    images = job.get_images()

    # Создаём экземплар для отрисовки масок:
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
    task = Task(task_id)
    task.create_path()
    for job_id in task.jobs_id:
        handle_job(job_id, different_path=task.path) # Добавляем путь к task.


def handle_project(project_id: int):
    """Обработка сущности project"""
    raise NotImplementedError()
