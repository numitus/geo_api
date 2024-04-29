from typing import Optional

from pydantic import BaseModel

from backend.model import Status, TaskResult


class TaskCreationResponse(BaseModel):
    status: Status
    task_id: str


class TaskResultResponse(TaskCreationResponse):
    data: Optional[TaskResult] = None
