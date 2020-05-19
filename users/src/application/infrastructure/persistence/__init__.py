from abc import ABCMeta, abstractmethod

from src.application.entity.health_check import HealthCheckStatus
from src.application.entity.user import ApplicationUser
from src.application.types import (
    Maybe,
    Either,
    SimpleConfig
)
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success
from src.domain.entity.user import DomainUser as DomainUser


class PersistenceInterface(metaclass=ABCMeta):
    # maybe having a better way of doing this later ;)
    class FetchBy:
        @abstractmethod
        def id(self, *, user_id: str) -> Either[Failure, ApplicationUser]: pass

        @abstractmethod
        def name(self, *, user_name: str) -> Either[Failure, ApplicationUser]: pass

        @abstractmethod
        def email(self, *, user_email: str) -> Either[Failure, ApplicationUser]: pass

    class UpdateBy:
        @abstractmethod
        def id(self, *, user_id: str, updated_user: DomainUser) -> Either[Failure, ApplicationUser]: pass

        @abstractmethod
        def name(self, *, user_name: str, updated_user: DomainUser) -> Either[Failure, ApplicationUser]: pass

        @abstractmethod
        def email(self, *, user_email: str, updated_user: DomainUser) -> Either[Failure, ApplicationUser]: pass

    class DeleteBy:
        @abstractmethod
        def id(self, *, user_id: str) -> Either[Failure, Success]: pass

        @abstractmethod
        def name(self, *, user_name: str) -> Either[Failure, Success]: pass

        @abstractmethod
        def email(self, *, user_email: str) -> Either[Failure, Success]: pass

    @abstractmethod
    def __init__(self, *, config: Maybe[SimpleConfig]) -> None:
        self.fetch_user_by = self._fetch_user_by()
        self.update_user_by = self._update_user_by()
        self.delete_user_by = self._delete_user_by()

    @staticmethod
    def from_domain_user_to_database_user(*, user: DomainUser, user_id: str) -> ApplicationUser:
        return ApplicationUser(
            id=user_id,
            name=user.name,
            age=user.age,
            email=user.email,
            password=user.password
        )

    @staticmethod
    def from_database_user_to_domain_user(*, user: ApplicationUser) -> DomainUser:
        return DomainUser(
            name=user.name,
            age=user.age,
            email=user.email,
            password=user.password
        )

    @abstractmethod
    def persist_user(self, *, user: DomainUser) -> Either[Failure, ApplicationUser]: pass

    @abstractmethod
    def _fetch_user_by(self) -> 'PersistenceInterface.FetchBy': pass

    @abstractmethod
    def _update_user_by(self) -> 'PersistenceInterface.UpdateBy': pass

    @abstractmethod
    def _delete_user_by(self) -> 'PersistenceInterface.DeleteBy': pass

    @abstractmethod
    def health_check(self) -> HealthCheckStatus: pass
