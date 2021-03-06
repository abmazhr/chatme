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
from src.application.usecase.user.add_access_token import AddAccessTokenUseCase
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.usecase.user.delete_user import DeleteUserUseCase
from src.application.usecase.user.fetch_access_token import FetchAccessTokenUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.application.usecase.user.update_user import UpdateUserUseCase


class RestApiInterface(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *,
                 config: Maybe[SimpleConfig],
                 host: str,
                 port: int,
                 routes: List[Route]) -> None:
        self.register_endpoints(routes=routes)
        self.register_generated_openid_docs(host=host, port=port)

    @abstractmethod
    def register_endpoints(self, *, routes: List[Route]) -> None: pass

    @abstractmethod
    def register_generated_openid_docs(self, *, host: str, port: int) -> None: pass

    @classmethod
    @abstractmethod
    def health_check(cls, *, services: List[Service]) -> Callable[..., JsonEntity.of(_type=_A)]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> JsonEntity.of(_type=_A): pass

        return wrapper

    @abstractmethod
    def open_api_schema(self) -> Callable[..., Any]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> Any: pass

        return wrapper

    @classmethod
    @abstractmethod
    def get_access_token(cls, *,
                         add_access_token_usecase: AddAccessTokenUseCase,
                         json_schema: Dict[str, Any],
                         json_schema_validator: JsonValidatorInterface) -> Callable[..., JsonEntity.of(_type=_A)]:
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
                 fetch_user_usecase: FetchUserUseCase,
                 fetch_access_token_usecase: FetchAccessTokenUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> JsonEntity.of(_type=_A): pass

        return wrapper

    @classmethod
    @abstractmethod
    def update_user(cls, *,
                    update_user_usecase: UpdateUserUseCase,
                    fetch_user_usecase: FetchUserUseCase,
                    fetch_access_token_usecase: FetchAccessTokenUseCase,
                    json_schema: Dict[str, Any],
                    json_schema_validator: JsonValidatorInterface) -> Callable[..., JsonEntity.of(_type=_A)]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> JsonEntity.of(_type=_A): pass

        return wrapper

    @classmethod
    @abstractmethod
    def delete_user(cls, *,
                    delete_user_usecase: DeleteUserUseCase,
                    fetch_user_usecase: FetchUserUseCase,
                    fetch_access_token_usecase: FetchAccessTokenUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        @abstractmethod
        def wrapper(*args, **kwargs) -> JsonEntity.of(_type=_A): pass

        return wrapper

    @abstractmethod
    def run(self, *, host: str, port: int, debug: bool, workers: int) -> None: pass
