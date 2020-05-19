from src.application.entity.user import ApplicationUser
from src.application.infrastructure.persistence import PersistenceInterface
from src.application.types import (
    Maybe,
    Either,
    SimpleConfig,
    List
)
from src.application.usecase import UseCaseInterface
from src.application.utilities.functions import exception_handler
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success
from src.domain.entity.user import DomainUser

_update_selectors: List[str] = ["id", "name", "email"]


class UpdateUserUseCase(UseCaseInterface):
    def __init__(self, *, config: Maybe[SimpleConfig], persistence: PersistenceInterface) -> None:
        self.__persistence = persistence
        super().__init__(config=config, persistence=persistence)

    @exception_handler
    def execute(self, *,
                update_by_selector: str,
                update_by_data: str,
                updated_user: DomainUser) -> Either[Failure, ApplicationUser]:
        if update_by_selector not in _update_selectors:
            return Failure(error=f"Update selector should be within this list {_update_selectors}")

        selector_mapping = {
            "id": self.__persistence.update_user_by.id,
            "name": self.__persistence.update_user_by.name,
            "email": self.__persistence.update_user_by.email
        }

        update_user_status: Either[Failure, ApplicationUser] = selector_mapping[update_by_selector](
            **{f"user_{update_by_selector}": update_by_data, "updated_user": updated_user}
        )
        return update_user_status
