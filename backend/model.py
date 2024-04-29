import enum
import uuid
from typing import Optional

from bunnet import Document, Indexed, init_bunnet
from pydantic import BaseModel, Field
from pymongo import MongoClient
from typing_extensions import Annotated

from backend.settings import settings


class Status(str, enum.Enum):
    PENDING = "running"
    COMPLETED = "done"
    FAILED = "failed"


class Point(BaseModel):
    name: str
    address: str


class Link(BaseModel):
    name: str
    distance: float


class Coordinate(BaseModel):
    name: str
    lon: float
    lat: float


class TaskResult(BaseModel):
    points: list[Point] = []
    links: list[Link] = []


class Task(Document):
    task_id: Annotated[str, Indexed(unique=True), Field(default_factory=lambda: str(uuid.uuid4()))]
    status: Status
    data: Optional[TaskResult] = None
    coordinates: list[Coordinate] = []


mongo_document_models = [Task]


def init_db():
    mongo_client = MongoClient(settings.mongo_host, settings.mongo_port)
    mongo_db = mongo_client[settings.mongo_db]
    init_bunnet(database=mongo_db, document_models=mongo_document_models)
