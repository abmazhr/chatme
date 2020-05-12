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

_delete_selectors: List[str] = ["id", "name", "email"]


class DeleteUserUseCase(UseCaseInterface):
    def __init__(self, *, config: Maybe[SimpleConfig], persistence: PersistenceInterface) -> None:
        self.__persistence = persistence
        super().__init__(config=config, persistence=persistence)

    @exception_handler
    def execute(self, *,
                delete_by_selector: str,
                delete_by_data: str) -> Either[Failure, ApplicationUser]:
        if delete_by_selector not in _delete_selectors:
            return Failure(error=f"Delete selector should be within this list {_delete_selectors}")

        selector_mapping = {
            "id": self.__persistence.delete_user_by.id,
            "name": self.__persistence.delete_user_by.name,
            "email": self.__persistence.delete_user_by.email
        }

        delete_user_status: Either[Failure, Success] = selector_mapping[delete_by_selector](
            **{f"user_{delete_by_selector}": delete_by_data}
        )
        return delete_user_status
