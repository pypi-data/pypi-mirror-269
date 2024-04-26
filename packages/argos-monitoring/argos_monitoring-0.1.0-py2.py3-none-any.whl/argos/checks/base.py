"""Various base classes for checks"""

from dataclasses import dataclass
from typing import Type, Union

import httpx
from pydantic import BaseModel

from argos.schemas.models import Task


class Status:
    """Possible statuses of the checks"""

    ON_CHECK = "on-check"
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"


class Severity:
    """Possible statuses of the checks’ results"""

    OK = "ok"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


# XXX We could name this Result, but is it could overlap with schemas.Result.
# Need to better define the naming around this.
# Status can be "Success" / "Failure" / "Error" or "On Check"
@dataclass
class Response:
    status: str
    context: dict

    @classmethod
    def new(cls, status, **kwargs):
        """Normalize results of checks."""
        if isinstance(status, bool):
            status = Status.SUCCESS if status else Status.FAILURE

        return cls(status=status, context=kwargs)


class BaseExpectedValue(BaseModel):
    expected: str

    def get_converted(self):
        return self.expected


class ExpectedIntValue(BaseExpectedValue):
    def get_converted(self):
        return int(self.expected)


class ExpectedStringValue(BaseExpectedValue):
    pass


class CheckNotFound(Exception):
    pass


class InvalidResponse(Exception):
    def __str__(self):
        return "The provided response is missing a 'status' key."


class BaseCheck:
    config: str
    expected_cls: Union[None, Type[BaseExpectedValue]] = None

    _registry = []  # type: ignore[var-annotated]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry.append(cls)

    @classmethod
    def get_registered_checks(cls):
        """Return existing checks"""
        return {c.config: c for c in cls._registry}

    @classmethod
    def get_registered_check(cls, name):
        """Get a check from its name"""
        check = cls.get_registered_checks().get(name)
        if not check:
            raise CheckNotFound(name)
        return check

    def __init__(self, http_client: httpx.AsyncClient, task: Task):
        self.http_client = http_client
        self.task = task

    @property
    def expected(self):
        """Convert the task’s class to simpler class"""
        if self.expected_cls is not None:
            return self.expected_cls(expected=self.task.expected).get_converted()
        return None

    def response(self, **kwargs):
        """Ensure that the response has a status and return a Response"""
        if "status" not in kwargs:
            raise InvalidResponse(kwargs)
        status = kwargs.pop("status")
        return Response.new(status, **kwargs)

    @classmethod
    async def finalize(cls, config, result, **context):
        """By default, the finalize considers that :

        - All FAILUREs should be reported as CRITICAL
        - All SUCCESS should be reported as OK
        - All ERRORS should be reported as UNKNOWN.

        This behaviour can be changed in each check, by defining the `finalize` method.
        XXX Allow this to be tweaked by the config.
        """
        if result.status == Status.SUCCESS:
            return result.status, Severity.OK
        if result.status == Status.ERROR:
            return result.status, Severity.UNKNOWN
        if result.status == Status.FAILURE:
            return result.status, Severity.CRITICAL
        if result.status == Status.ON_CHECK:
            msg = (
                "Status is 'on-check', but the Check class "
                "didn't provide a finalize() method."
            )
            raise ValueError(msg)

    @classmethod
    def get_description(cls, config):
        return cls.__doc__ or ""


def get_registered_check(name):
    return BaseCheck.get_registered_check(name)


def get_registered_checks():
    return BaseCheck.get_registered_checks()
