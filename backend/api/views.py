from flask import jsonify, request

from backend.api.schema import TaskCreationResponse, TaskResultResponse
from backend.lib.parser import parse_csv
from backend.model import Status, Task
from celeryapp.tasks.tasks import process_task

from . import api


@api.route("/calculateDistances", methods=["POST"])
def calculate_distances():
    """This endpoint is used to create a new task to calculate distances between coordinates."""
    if len(request.files) == 0:
        return jsonify({"error": "File is not uploaded"}), 400
    elif len(request.files) > 1:
        return jsonify({"error": "Only one file should be uploaded"}), 400

    file = list(request.files.values())[0]
    content = file.stream.read().decode("utf-8")
    try:
        coordinates = parse_csv(content)
    except:  # noqa
        return jsonify({"error": "Invalid CSV file"}), 400
    task = Task(status=Status.PENDING, coordinates=coordinates).insert()

    process_task.delay(str(task.task_id))

    return jsonify(TaskCreationResponse(**task.model_dump()).dict())


@api.route("/getResult", methods=["GET"])
def get_result():
    """This endpoint is used to retrieve the result of a task."""
    # Retrieve task ID from query parameters
    task_id = request.args.get("task_id")
    if task_id is None:
        return jsonify({"error": "Task ID is required"}), 400
    # Retrieve task details from database
    task = Task.find({"task_id": task_id}).first_or_none()
    if task:
        return jsonify(TaskResultResponse(**task.model_dump(exclude_none=True)).model_dump(exclude_none=True))
    else:
        return jsonify({"error": "Task not found"}), 404
