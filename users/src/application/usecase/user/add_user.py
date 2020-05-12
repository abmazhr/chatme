from src.application.entity.user import ApplicationUser
from src.application.infrastructure.persistence import PersistenceInterface
from src.application.types import (
    Maybe,
    Either,
    SimpleConfig
)
from src.application.usecase import UseCaseInterface
from src.application.utilities.functions import exception_handler
from src.domain.entity.failure import Failure
from src.domain.entity.user import DomainUser as DomainUser, create_user


class AddUserUseCase(UseCaseInterface):
    def __init__(self, *, config: Maybe[SimpleConfig], persistence: PersistenceInterface) -> None:
        super().__init__(config=config, persistence=persistence)
        self.__persistence = persistence

    @exception_handler
    def execute(self, *,
                username: str,
                age: int,
                password: str,
                email: Maybe[str]) -> Either[Failure, ApplicationUser]:
        domain_user_creation_status: Either[Failure, DomainUser] = create_user(
            name=username,
            age=age,
            password=password,
            email=email
        )
        if isinstance(domain_user_creation_status, Failure):
            return Failure(error=domain_user_creation_status.error)

        database_user_creation_status: Either[Failure, ApplicationUser] = self.__persistence.persist_user(
            user=domain_user_creation_status
        )
        if isinstance(database_user_creation_status, Failure):
            return Failure(error=database_user_creation_status.error)

        return database_user_creation_status
