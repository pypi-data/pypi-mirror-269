from typing import Literal, Union


def string_to_duration(
    value: str, target: Literal["days", "hours", "minutes"]
) -> Union[int, float]:
    """Convert a string to a number of hours, days or minutes"""
    num = int("".join(filter(str.isdigit, value)))

    # It's not possible to convert from a smaller unit to a greater one:
    # - hours and minutes cannot be converted to days
    # - minutes cannot be converted to hours
    if (target == "days" and ("h" in value or "m" in value.replace("mo", ""))) or (
        target == "hours" and "m" in value.replace("mo", "")
    ):
        msg = (
            "Durations cannot be converted from a smaller to a greater unit. "
            f"(trying to convert '{value}' to {target})"
        )
        raise ValueError(msg, value)

    # Consider we're converting to minutes, do the eventual multiplication at the end.
    if "h" in value:
        num = num * 60
    elif "d" in value:
        num = num * 60 * 24
    elif "w" in value:
        num = num * 60 * 24 * 7
    elif "mo" in value:
        num = num * 60 * 24 * 30  # considers 30d in a month
    elif "y" in value:
        num = num * 60 * 24 * 365  # considers 365d in a year
    elif "m" not in value:
        raise ValueError("Invalid duration value", value)

    if target == "hours":
        return num / 60
    if target == "days":
        return num / 60 / 24

    # target == "minutes"
    return num
