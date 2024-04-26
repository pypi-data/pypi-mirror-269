import pytest

from argos.schemas.config import SSL, WebsitePath


def test_ssl_duration_parsing():
    data = {"thresholds": [{"2d": "warning"}, {"3w": "error"}]}

    # Test the validation and parsing of SSL model
    ssl_object = SSL(**data)
    assert len(ssl_object.thresholds) == 2
    assert ssl_object.thresholds == [(2, "warning"), (21, "error")]

    # Test the constraint on severity
    with pytest.raises(ValueError):
        erroneous_data = {"thresholds": [{"1d": "caution"}, {"1w": "danger"}]}
        SSL(**erroneous_data)


def test_path_parsing_transforms_to_tuples():
    data = {"path": "/", "checks": [{"body-contains": "youpi"}, {"status-is": "200"}]}
    path = WebsitePath(**data)
    assert len(path.checks) == 2
    assert path.checks == [("body-contains", "youpi"), ("status-is", "200")]


def test_path_ensures_check_exists():
    with pytest.raises(ValueError):
        erroneous_data = {
            "path": "/",
            "checks": [{"non-existing-key": "youpi"}, {"status-is": "200"}],
        }
        WebsitePath(**erroneous_data)


def test_expected_accepts_and_convert_ints():
    data = {"path": "/", "checks": [{"body-contains": "youpi"}, {"status-is": 200}]}
    path = WebsitePath(**data)
    assert len(path.checks) == 2
    assert path.checks == [("body-contains", "youpi"), ("status-is", "200")]
