from pytest import fixture

from src.application.infrastructure.persistence import PersistenceInterface
from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.domain.entity.failure import Failure
from src.domain.entity.user import DomainUser as DomainUser
from test.utilities.user import generate_valid_domain_user


@fixture(scope='function')
def setup():
    db = InMemoryDatabase(
        config=None
    )
    add_usecase = AddUserUseCase(
        config=None,
        persistence=db
    )
    fetch_usecase = FetchUserUseCase(
        config=None,
        persistence=db
    )

    created_domain_user = generate_valid_domain_user()
    add_usecase.execute(
        username=created_domain_user.name,
        age=created_domain_user.age,
        password=created_domain_user.password,
        email=created_domain_user.email
    )

    yield fetch_usecase, created_domain_user
    del add_usecase, fetch_usecase


def test_valid_fetch_user(setup):
    usecase, created_domain_user = setup
    usecase: FetchUserUseCase
    created_domain_user: DomainUser

    # by id
    assert usecase.execute(
        fetch_by_selector="id",
        fetch_by_data="0"
    ) == PersistenceInterface.from_domain_user_to_database_user(
        user=created_domain_user,
        user_id="0"
    )

    # by name
    assert usecase.execute(
        fetch_by_selector="name",
        fetch_by_data="test"
    ) == PersistenceInterface.from_domain_user_to_database_user(
        user=created_domain_user,
        user_id="0"
    )
    # by email
    assert usecase.execute(
        fetch_by_selector="email",
        fetch_by_data="test@test.com"
    ) == PersistenceInterface.from_domain_user_to_database_user(
        user=created_domain_user,
        user_id="0"
    )


def test_invalid_fetch_user(setup):
    usecase, created_domain_user = setup
    usecase: FetchUserUseCase
    created_domain_user: DomainUser

    # by invalid selector
    assert usecase.execute(
        fetch_by_selector="invalid_selector",
        fetch_by_data="invalid_data(doesn't matter)"
    ) == Failure(error="Fetch selector should be within this list ['id', 'name', 'email']")

    # by id
    assert usecase.execute(
        fetch_by_selector="id",
        fetch_by_data="1"
    ) == Failure(error='There is no user with id 1 to be fetched')

    # by name
    assert usecase.execute(
        fetch_by_selector="name",
        fetch_by_data="invalid"
    ) == Failure(error='There is no user with name invalid to be fetched')
    # by email
    assert usecase.execute(
        fetch_by_selector="email",
        fetch_by_data="invalid"
    ) == Failure(error='There is no user with email invalid to be fetched')
