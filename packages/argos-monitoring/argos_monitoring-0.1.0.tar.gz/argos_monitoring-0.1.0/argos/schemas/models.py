"""Pydantic schemas for data

For database models, see argos.server.models.
"""
import traceback
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

# XXX Refactor using SQLModel to avoid duplication of model data


class Task(BaseModel):
    """A task corresponds to a check to execute"""

    id: int
    url: str
    domain: str
    check: str
    expected: str
    selected_at: datetime | None
    selected_by: str | None

    model_config = ConfigDict(from_attributes=True)

    def __str__(self):
        task_id = self.id
        url = self.url
        check = self.check
        return f"Task ({task_id}): {url} - {check}"


class SerializableException(BaseModel):
    """Task exception"""

    error_message: str
    error_type: str
    error_details: str

    @staticmethod
    def from_exception(err: BaseException):
        return SerializableException(
            error_message=str(err),
            error_type=str(type(err).__name__),
            error_details=traceback.format_exc(),
        )


class AgentResult(BaseModel):
    """Task’s result sent by agent"""

    task_id: int
    # The on-check status means that the service needs to finish the check
    # and will then determine the severity.
    status: Literal["success", "failure", "error", "on-check"]
    context: dict | SerializableException
