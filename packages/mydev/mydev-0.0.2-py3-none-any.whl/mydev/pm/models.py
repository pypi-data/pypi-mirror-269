from enum import Enum

from sqlmodel import Field, SQLModel


class Status(str, Enum):
    creating = "creating"
    running = "running"
    failed = "failed"
    completed = "completed"


class Process(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cmd: str
    status: Status = Status.creating
    pid: int | None = None
    alias: str | None = None
