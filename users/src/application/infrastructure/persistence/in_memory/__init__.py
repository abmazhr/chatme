from src.application.entity.user import ApplicationUser
from src.application.infrastructure.persistence import PersistenceInterface
from src.application.types import (
    Maybe,
    Either,
    SimpleConfig
)
from src.application.utilities.functions import exception_handler
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success
from src.domain.entity.user import DomainUser as DomainUser


class InMemoryDatabase(PersistenceInterface):
    def __init__(self, *, config: Maybe[SimpleConfig]) -> None:
        self.__db = dict(ids={}, names={}, emails={})
        self.__last_id = 0  # just simple increment but in real db it's more complicated xD
        super().__init__(config=config)
        """
        For example the DB will look like these references
        {
            "ids": {
                    "0": {
                        "name": "user_1",
                        "age": 26,
                        "email": "test1@test.com",
                        "password": "encrypted_password"
                    }
            },
            "names": {
                "user_1": 0           # which is the id (simple way as symlinks on Unix, may improve later)
            },
            "emails": {
                "test1@test.com": 0   # which is the id (simple way as symlinks on Unix, may improve later)
            }
        }
        """

    # maybe later will modularize the functions in modules to be easier to maintain ;)

    @exception_handler
    def persist_user(self, *, user: DomainUser) -> Either[Failure, ApplicationUser]:
        persisted_user = PersistenceInterface.from_domain_user_to_database_user(
            user=user,
            user_id=str(self.__last_id)
        )
        self.__db['ids'][str(self.__last_id)] = persisted_user
        self.__db['names'][user.name] = str(self.__last_id)
        self.__db['emails'][user.email] = str(self.__last_id)
        self.__last_id += 1

        return persisted_user

    def _fetch_user_by(self) -> 'PersistenceInterface.FetchBy':
        db = self.__db

        class InMemoryFetchBy(PersistenceInterface.FetchBy):
            @exception_handler
            def id(self, *, user_id: str) -> Either[Failure, ApplicationUser]:
                fetch_status: Maybe[ApplicationUser] = db["ids"].get(user_id)
                if isinstance(fetch_status, ApplicationUser):
                    return fetch_status

                return Failure(error=f"There is no user with id {user_id} to be fetched")

            @exception_handler
            def name(self, *, user_name: str) -> Either[Failure, ApplicationUser]:
                user_id: str = db["names"].get(user_name)
                if user_id is not None:
                    user: ApplicationUser = db["ids"][user_id]
                    return user

                return Failure(error=f"There is no user with name {user_name} to be fetched")

            @exception_handler
            def email(self, *, user_email: str) -> Either[Failure, ApplicationUser]:
                user_id: str = db["emails"].get(user_email)
                if user_id is not None:
                    user: ApplicationUser = db["ids"][user_id]
                    return user

                return Failure(error=f"There is no user with email {user_email} to be fetched")

        return InMemoryFetchBy()

    def _update_user_by(self) -> 'PersistenceInterface.UpdateBy':
        db = self.__db

        class InMemoryUpdateBy(PersistenceInterface.UpdateBy):
            @exception_handler
            def id(self, *, user_id: str, updated_user: DomainUser) -> Either[Failure, Success]:
                fetch_status: Maybe[ApplicationUser] = db["ids"].get(user_id)
                if isinstance(fetch_status, ApplicationUser):
                    db["ids"][fetch_status.id] = PersistenceInterface.from_domain_user_to_database_user(
                        user=updated_user,
                        user_id=fetch_status.id
                    )

                    return Success()

                return Failure(error=f"There is no user with id {user_id} to be updated")

            def name(self, *, user_name: str, updated_user: DomainUser) -> Either[Failure, Success]:
                user_id: Maybe[str] = db["names"].get(user_name)
                if user_id is not None:
                    db["ids"][user_id] = PersistenceInterface.from_domain_user_to_database_user(
                        user=updated_user,
                        user_id=user_id
                    )

                    return Success()

                return Failure(error=f"There is no user with name {user_name} to be updated")

            def email(self, *, user_email: str, updated_user: DomainUser) -> Either[Failure, Success]:
                user_id: Maybe[str] = db["emails"].get(user_email)
                if user_id is not None:
                    db["ids"][user_id] = PersistenceInterface.from_domain_user_to_database_user(
                        user=updated_user,
                        user_id=user_id
                    )

                    return Success()

                return Failure(error=f"There is no user with email {user_email} to be updated")

        return InMemoryUpdateBy()

    def _delete_user_by(self) -> 'PersistenceInterface.DeleteBy':
        db = self.__db

        class InMemoryDeleteBy(PersistenceInterface.DeleteBy):
            @exception_handler
            def __inner_delete_user(self, *, user: ApplicationUser) -> Either[Failure, Success]:
                del db["ids"][user.id]
                del db["names"][user.name]
                del db["emails"][user.email]

                return Success()

            @exception_handler
            def id(self, *, user_id: str) -> Either[Failure, Success]:
                fetch_status: Maybe[ApplicationUser] = db["ids"].get(user_id)
                if isinstance(fetch_status, ApplicationUser):
                    self.__inner_delete_user(user=fetch_status)
                    return Success()

                return Failure(error=f"There is no user with id {user_id} to be deleted")

            @exception_handler
            def name(self, *, user_name: str) -> Either[Failure, Success]:
                user_id: Maybe[str] = db["names"].get(user_name)
                if user_id is not None:
                    self.__inner_delete_user(user=db["ids"][user_id])
                    return Success()

                return Failure(error=f"There is no user with name {user_name} to be deleted")

            @exception_handler
            def email(self, *, user_email: str) -> Either[Failure, Success]:
                user_id: Maybe[str] = db["emails"].get(user_email)
                if user_id is not None:
                    self.__inner_delete_user(user=db["ids"][user_id])
                    return Success()

                return Failure(error=f"There is no user with email {user_email} to be deleted")

        return InMemoryDeleteBy()


db = InMemoryDatabase(config=None)
print(db)
