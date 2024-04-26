import datetime
import ssl
from unittest.mock import MagicMock

import httpx
import pytest

from argos.checks import SSLCertificateExpiration
from argos.schemas import Task


@pytest.fixture
def now():
    return datetime.datetime.now()


@pytest.fixture
def httpx_extensions_ssl():
    """Returns the httpx extension dict used by the SSL verification check,
    to be used when mocking the client responses"""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    ssl_obj = MagicMock()
    ssl_obj.getpeercert.return_value = {"notAfter": "Jan 25 20:35:00 2024 GMT"}
    network_stream = MagicMock()
    network_stream.get_extra_info = MagicMock(return_value=ssl_obj)
    return {"network_stream": network_stream}


@pytest.fixture
def ssl_task(now):
    return Task(
        id=1,
        url="https://example.org",
        domain="https://example.org",
        check="ssl-certificate-expiration",
        expected="on-check",
        selected_at=now,
        selected_by="pytest",
    )


@pytest.mark.parametrize("http_status", ["200", "300", "400", "500"])
@pytest.mark.asyncio
async def test_ssl_check_accepts_statuts(
    respx_mock, ssl_task, httpx_extensions_ssl, http_status
):
    respx_mock.get("https://example.org").mock(
        return_value=httpx.Response(http_status, extensions=httpx_extensions_ssl),
    )
    async with httpx.AsyncClient() as client:
        check = SSLCertificateExpiration(client, ssl_task)
        check_response = await check.run()
        assert check_response.status == "on-check"
