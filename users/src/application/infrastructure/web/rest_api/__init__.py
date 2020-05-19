from abc import ABCMeta, abstractmethod

from src.application.entity.service import Service
from src.application.infrastructure.web.entity.json import _A, JsonEntity
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.validation import JsonValidatorInterface
from src.application.types import (
    Maybe,
    SimpleConfig,
    Callable,
    List,
    Dict,
    Any
)
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.usecase.user.delete_user import DeleteUserUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.application.usecase.user.update_user import UpdateUserUseCase


class RestApiInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *,
                 config: Maybe[SimpleConfig],
                 routes: List[Route]) -> None:
        self.register_endpoints(routes=routes)

    @abstractmethod
    def register_endpoints(self, *, routes: List[Route]) -> None: pass

    @classmethod
    @abstractmethod
    def health_check(cls, *, services: List[Service]) -> Callable[..., JsonEntity.of(_type=_A)]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> JsonEntity.of(_type=_A): pass

        return wrapper

    @classmethod
    @abstractmethod
    def post_user(cls, *,
                  add_user_usecase: AddUserUseCase,
                  json_schema: Dict[str, Any],
                  json_schema_validator: JsonValidatorInterface) -> Callable[..., JsonEntity.of(_type=_A)]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> JsonEntity.of(_type=_A): pass

        return wrapper

    @classmethod
    @abstractmethod
    def get_user(cls, *,
                 fetch_user_usecase: FetchUserUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> JsonEntity.of(_type=_A): pass

        return wrapper

    @classmethod
    @abstractmethod
    def update_user(cls, *,
                    update_user_usecase: UpdateUserUseCase,
                    json_schema: Dict[str, Any],
                    json_schema_validator: JsonValidatorInterface) -> Callable[..., JsonEntity.of(_type=_A)]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> JsonEntity.of(_type=_A): pass

        return wrapper

    @classmethod
    @abstractmethod
    def delete_user(cls, *,
                    delete_user_usecase: DeleteUserUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> JsonEntity.of(_type=_A): pass

        return wrapper

    @abstractmethod
    def run(self, *, host: str, port: int, debug: bool, workers: int) -> None: pass
