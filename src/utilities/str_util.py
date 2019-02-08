"""
"""
from typing import Any


def safeStrip(value: Any) -> Any:
    if isinstance(value, str):
        newValue = value.strip()
        return newValue
    else:
        return value
