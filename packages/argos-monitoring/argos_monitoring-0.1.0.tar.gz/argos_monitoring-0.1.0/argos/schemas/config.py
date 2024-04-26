"""Pydantic schemas for configuration

For database models, see argos.server.models.
"""
from typing import Dict, List, Literal, Optional, Tuple

from pydantic import (
    BaseModel,
    ConfigDict,
    HttpUrl,
    StrictBool,
    EmailStr,
    PositiveInt,
    field_validator,
)
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from argos.schemas.utils import string_to_duration

Severity = Literal["warning", "error", "critical", "unknown"]


def parse_threshold(value):
    """Parse duration threshold for SSL certificate validity"""
    for duration_str, severity in value.items():
        days = string_to_duration(duration_str, "days")
        # Return here because it's one-item dicts.
        return (days, severity)


class SSL(BaseModel):
    thresholds: List[Annotated[Tuple[int, Severity], BeforeValidator(parse_threshold)]]


class WebsiteCheck(BaseModel):
    key: str
    value: str | List[str] | Dict[str, str]
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, str):
            return {"expected": value}
        if isinstance(value, dict):
            return value
        if isinstance(value, list):
            return {"expected": value}

        raise ValueError("Invalid type")


def parse_checks(value):
    """Check that checks are valid (i.e. registered) checks"""

    # To avoid circular imports
    from argos.checks import get_registered_checks

    available_names = get_registered_checks().keys()

    for name, expected in value.items():
        if name not in available_names:
            msg = f"Check should be one of f{available_names}. ({name} given)"
            raise ValueError(msg)
        if isinstance(expected, int):
            expected = str(expected)
        return (name, expected)


class WebsitePath(BaseModel):
    path: str
    checks: List[
        Annotated[
            Tuple[str, str],
            BeforeValidator(parse_checks),
        ]
    ]


class Website(BaseModel):
    domain: HttpUrl
    frequency: Optional[int] = None
    paths: List[WebsitePath]

    @field_validator("frequency", mode="before")
    def parse_frequency(cls, value):
        """Convert the configured frequency to minutes"""
        if value:
            return string_to_duration(value, "minutes")

        return None


class Service(BaseModel):
    """List of agents’ token"""

    secrets: List[str]


class MailAuth(BaseModel):
    """Mail authentication configuration"""

    login: str
    password: str


class Mail(BaseModel):
    """Mail configuration"""

    mailfrom: EmailStr
    host: str = "127.0.0.1"
    port: PositiveInt = 25
    ssl: StrictBool = False
    starttls: StrictBool = False
    auth: Optional[MailAuth] = None
    addresses: List[EmailStr]


class Alert(BaseModel):
    """List of way to handle alerts, by severity"""

    ok: List[str]
    warning: List[str]
    critical: List[str]
    unknown: List[str]


class GotifyUrl(BaseModel):
    url: HttpUrl
    tokens: List[str]


class General(BaseModel):
    """Frequency for the checks and alerts"""

    frequency: int
    alerts: Alert
    mail: Optional[Mail] = None
    gotify: Optional[List[GotifyUrl]] = None

    @field_validator("frequency", mode="before")
    def parse_frequency(cls, value):
        """Convert the configured frequency to minutes"""
        return string_to_duration(value, "minutes")


class Config(BaseModel):
    general: General
    service: Service
    ssl: SSL
    websites: List[Website]
