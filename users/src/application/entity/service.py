from src.application.types import NamedTuple, TypeVar

_A = TypeVar("_A")


class Service(NamedTuple):
    service_instance: _A
