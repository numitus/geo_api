import logging

from backend.lib.geocode_service import GeocodeService
from backend.lib.link_service import get_links
from backend.model import Point, Status, Task, TaskResult
from backend.settings import settings
from celeryapp.app import app


def _process_task(task: Task) -> None:
    for point in task.coordinates:
        logging.info(f"Processing point {point}")
    points = GeocodeService(settings.geocode_api).batch_request(task.coordinates)
    task.data = TaskResult()
    task.data.points = [
        Point(name=coordinate.name, address=address) for coordinate, address in zip(task.coordinates, points)
    ]
    task.data.links = get_links(task.coordinates)
    task.status = Status.COMPLETED
    task.save()


@app.task
def process_task(task_id: str) -> None:
    """Process task with given ID and update its status"""
    logging.info(f"Processing coordinates for task {task_id}")
    task = Task.find({"task_id": task_id}).first_or_none()
    logging.info(f"Task {task.status} retrieved")
    if task is None:
        logging.error(f"Task {task_id} not found")
        return

    try:
        _process_task(task)
    except Exception as e:
        logging.error(f"Task {task_id} failed: {e}")
        task.status = Status.FAILED
        task.save()
        return
    logging.info(f"Task {task_id} completed")
