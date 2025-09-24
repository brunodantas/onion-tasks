"""
This module defines Data Transfer Objects (DTOs) used in the use cases layer.
"""

class Result:
    pass


class Success(Result):
    def __init__(self, value: object):
        self.value = value

    __match_args__ = ("value",)

    def __repr__(self) -> str:
        return f"Success(value={self.value})"


class Failure(Result):
    def __init__(self, error: str):
        self.error = error

    __match_args__ = ("error",)

    def __repr__(self) -> str:
        return f"Failure(error={self.error})"
