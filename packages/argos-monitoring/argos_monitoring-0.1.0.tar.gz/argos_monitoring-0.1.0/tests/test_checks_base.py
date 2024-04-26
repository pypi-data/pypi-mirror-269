from argos.checks.base import Response, Status


def test_response_failure_with_context():
    resp = Response.new(False, some="context", another=True)
    assert resp.status == Status.FAILURE
    assert resp.context == {"some": "context", "another": True}


def test_response_success():
    resp = Response.new(True)
    assert resp.status == Status.SUCCESS


def test_response_on_check_with_context():
    resp = Response.new(Status.ON_CHECK, expires_in=3)
    assert resp.status == Status.ON_CHECK
    assert resp.status == "on-check"
    assert resp.context == {"expires_in": 3}
