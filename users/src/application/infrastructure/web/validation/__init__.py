from abc import ABCMeta, abstractmethod

from src.application.types import (
    Maybe,
    Either,
    Dict,
    Any,
    SimpleConfig
)
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success


class JsonValidatorInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *,
                 config: Maybe[SimpleConfig]) -> None: pass

    @abstractmethod
    def validate(self, *,
                 schema: Dict[str, Any],
                 data: Dict[str, Any]) -> Either[Failure, Success]: pass
