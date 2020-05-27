from src.application.infrastructure.web.entity.access_token import AccessToken
from src.application.infrastructure.persistence import PersistenceInterface
from src.application.types import (
    Maybe,
    Either,
    SimpleConfig
)
from src.application.usecase import UseCaseInterface
from src.application.utilities.functions import exception_handler
from src.domain.entity.failure import Failure


class AddAccessTokenUseCase(UseCaseInterface):
    def __init__(self, *,
                 config: Maybe[SimpleConfig],
                 persistence: PersistenceInterface) -> None:
        self.__persistence = persistence
        super().__init__(config=config, persistence=persistence)

    @exception_handler
    def execute(self, *,
                username: str,
                password: str) -> Either[Failure, AccessToken]:
        return self.__persistence.persist_access_token(
            username=username,
            password=password
        )
