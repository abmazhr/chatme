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

_fetch_selectors: List[str] = ["id", "name", "email"]


class FetchUserUseCase(UseCaseInterface):
    def __init__(self, *, config: Maybe[SimpleConfig], persistence: PersistenceInterface) -> None:
        self.__persistence = persistence
        super().__init__(config=config, persistence=persistence)

    @exception_handler
    def execute(self, *,
                fetch_by_selector: str,
                fetch_by_data: str) -> Either[Failure, ApplicationUser]:
        if fetch_by_selector not in _fetch_selectors:
            return Failure(error=f"Fetch selector should be within this list {_fetch_selectors}")

        selector_mapping = {
            "id": self.__persistence.fetch_user_by.id,
            "name": self.__persistence.fetch_user_by.name,
            "email": self.__persistence.fetch_user_by.email
        }

        fetch_user_status: Either[Failure, ApplicationUser] = selector_mapping[fetch_by_selector](
            **{f"user_{fetch_by_selector}": fetch_by_data}
        )
        return fetch_user_status
