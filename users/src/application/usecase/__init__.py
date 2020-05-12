from abc import ABCMeta, abstractmethod
from typing import Any

from src.application.infrastructure.persistence import PersistenceInterface
from src.application.types import (
    SimpleConfig,
    Maybe,
    Either
)
from src.domain.entity.failure import Failure


class UseCaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *,
                 config: Maybe[SimpleConfig],
                 persistence: PersistenceInterface) -> None: pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> Either[Failure, Any]: pass
