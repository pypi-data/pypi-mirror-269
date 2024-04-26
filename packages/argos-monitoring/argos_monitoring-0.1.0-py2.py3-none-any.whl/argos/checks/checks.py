"""Define the available checks"""

from datetime import datetime

from argos.checks.base import (
    BaseCheck,
    ExpectedIntValue,
    ExpectedStringValue,
    Severity,
    Status,
)


class HTTPStatus(BaseCheck):
    """Checks that the HTTP status code is the expected one."""

    config = "status-is"
    expected_cls = ExpectedIntValue

    async def run(self) -> dict:
        # XXX Get the method from the task
        task = self.task
        response = await self.http_client.request(
            method="get", url=task.url, timeout=60
        )

        return self.response(
            status=response.status_code == self.expected,
            expected=self.expected,
            retrieved=response.status_code,
        )


class HTTPBodyContains(BaseCheck):
    """Checks that the HTTP body contains the expected string."""

    config = "body-contains"
    expected_cls = ExpectedStringValue

    async def run(self) -> dict:
        response = await self.http_client.request(
            method="get", url=self.task.url, timeout=60
        )
        return self.response(status=self.expected in response.text)


class SSLCertificateExpiration(BaseCheck):
    """Checks that the SSL certificate will not expire soon."""

    config = "ssl-certificate-expiration"
    expected_cls = ExpectedStringValue

    async def run(self):
        """Returns the number of days in which the certificate will expire."""
        response = await self.http_client.get(self.task.url, timeout=60)

        network_stream = response.extensions["network_stream"]
        ssl_obj = network_stream.get_extra_info("ssl_object")
        cert = ssl_obj.getpeercert()

        not_after = datetime.strptime(cert.get("notAfter"), "%b %d %H:%M:%S %Y %Z")
        expires_in = (not_after - datetime.now()).days

        return self.response(status=Status.ON_CHECK, expires_in=expires_in)

    @classmethod
    async def finalize(cls, config, result, **context):
        if result.status != Status.ON_CHECK:
            return result.status, Severity.WARNING

        if "expires_in" in context:
            thresholds = config.ssl.thresholds
            thresholds.sort()
            for days, severity in thresholds:
                if context["expires_in"] < days:
                    return Status.FAILURE, severity
            return Status.SUCCESS, Severity.OK

        raise ValueError(
            "The SSLCertificateExpiration check didn't provide an 'expires_in' "
            "context variable."
        )

    @classmethod
    def get_description(cls, config):
        thresholds = config.ssl.thresholds
        thresholds.sort()
        string = SSLCertificateExpiration.__doc__ + "\n"
        for days, severity in thresholds:
            string += f"- {severity} if expiration in less than {days} days\n"
        return string
