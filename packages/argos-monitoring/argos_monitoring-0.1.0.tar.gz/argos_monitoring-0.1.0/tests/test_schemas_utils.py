import pytest

from argos.schemas.utils import string_to_duration


def test_string_to_duration_days():
    assert string_to_duration("1d", target="days") == 1
    assert string_to_duration("1w", target="days") == 7
    assert string_to_duration("3w", target="days") == 21
    assert string_to_duration("3mo", target="days") == 90
    assert string_to_duration("1y", target="days") == 365

    with pytest.raises(ValueError):
        string_to_duration("3h", target="days")

    with pytest.raises(ValueError):
        string_to_duration("1", target="days")


def test_string_to_duration_hours():
    assert string_to_duration("1h", target="hours") == 1
    assert string_to_duration("1d", target="hours") == 24
    assert string_to_duration("1w", target="hours") == 7 * 24
    assert string_to_duration("3w", target="hours") == 21 * 24
    assert string_to_duration("3mo", target="hours") == 3 * 30 * 24

    with pytest.raises(ValueError):
        string_to_duration("1", target="hours")


def test_string_to_duration_minutes():
    assert string_to_duration("1m", target="minutes") == 1
    assert string_to_duration("1h", target="minutes") == 60
    assert string_to_duration("1d", target="minutes") == 60 * 24
    assert string_to_duration("3mo", target="minutes") == 60 * 24 * 30 * 3

    with pytest.raises(ValueError):
        string_to_duration("1", target="minutes")


def test_conversion_to_greater_units_throws():
    # hours and minutes cannot be converted to days
    with pytest.raises(ValueError):
        string_to_duration("1h", target="days")

    with pytest.raises(ValueError):
        string_to_duration("1m", target="days")

    # minutes cannot be converted to hours
    with pytest.raises(ValueError):
        string_to_duration("1m", target="hours")
