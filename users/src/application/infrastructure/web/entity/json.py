from abc import ABCMeta

from src.application.types import (
    TypeVar
)

_A = TypeVar("_A")


class JsonEntity(metaclass=ABCMeta):
    @staticmethod
    def of(*, _type: _A): return _type
