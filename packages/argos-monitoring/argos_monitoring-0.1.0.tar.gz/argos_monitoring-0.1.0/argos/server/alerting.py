import ssl
import smtplib

from typing import List
from urllib.parse import urlparse

import httpx

from argos.checks.base import Severity
from argos.logging import logger
from argos.schemas.config import Config, Mail, GotifyUrl

# XXX Implement mail alerts https://framagit.org/framasoft/framaspace/argos/-/issues/15
# XXX Implement gotify alerts https://framagit.org/framasoft/framaspace/argos/-/issues/16


def handle_alert(config: Config, result, task, severity, old_severity, request):
    """Dispatch alert through configured alert channels"""

    if "local" in getattr(config.general.alerts, severity):
        logger.error(
            "Alerting stub: task=%i, status=%s, severity=%s",
            task.id,
            result.status,
            severity,
        )

    if config.general.mail is not None and "mail" in getattr(
        config.general.alerts, severity
    ):
        notify_by_mail(
            result, task, severity, old_severity, config.general.mail, request
        )

    if config.general.gotify is not None and "gotify" in getattr(
        config.general.alerts, severity
    ):
        notify_with_gotify(
            result, task, severity, old_severity, config.general.gotify, request
        )


def notify_by_mail(
    result, task, severity: str, old_severity: str, config: Mail, request
) -> None:
    logger.debug("Will send mail notification")

    msg = f"""\
URL:    {task.url}
Check:  {task.check}
Status: {severity}
Time:   {result.submitted_at}
Previous status: {old_severity}

See results of task on {request.url_for('get_task_results_view', task_id=task.id)}
"""

    mail = f"""\
Subject: [Argos] {urlparse(task.url).netloc}: status {severity}

{msg}"""

    if config.ssl:
        logger.debug("Mail notification: SSL")
        context = ssl.create_default_context()
        smtp = smtplib.SMTP_SSL(host=config.host, port=config.port, context=context)
    else:
        smtp = smtplib.SMTP(
            host=config.host,  # type: ignore
            port=config.port,
        )
        if config.starttls:
            logger.debug("Mail notification: STARTTLS")
            context = ssl.create_default_context()
            smtp.starttls(context=context)

    if config.auth is not None:
        logger.debug("Mail notification: authentification")
        smtp.login(config.auth.login, config.auth.password)

    for address in config.addresses:
        logger.debug("Sending mail to %s", address)
        logger.debug(msg)
        smtp.sendmail(config.mailfrom, address, mail)


def notify_with_gotify(
    result, task, severity: str, old_severity: str, config: List[GotifyUrl], request
) -> None:
    logger.debug("Will send gotify notification")
    headers = {"accept": "application/json", "content-type": "application/json"}

    priority = 9
    icon = "❌"
    if severity == Severity.OK:
        priority = 1
        icon = "✅"
    elif severity == Severity.WARNING:
        priority = 5
        icon = "⚠️"

    subject = f"{icon} {urlparse(task.url).netloc}: status {severity}"
    msg = f"""\
URL:    {task.url}
Check:  {task.check}
Status: {severity}
Time:   {result.submitted_at}
Previous status: {old_severity}

See results of task on {request.url_for('get_task_results_view', task_id=task.id)}
"""

    payload = {"title": subject, "message": msg, "priority": priority}

    for url in config:
        logger.debug("Sending gotify message(s) to %s", url)
        for token in url.tokens:
            try:
                res = httpx.post(
                    f"{url.url}message",
                    params={"token": token},
                    headers=headers,
                    json=payload,
                )
                res.raise_for_status()
            except httpx.RequestError as err:
                logger.error(
                    "An error occurred while sending a message to %s with token %s",
                    err.request.url,
                    token,
                )
