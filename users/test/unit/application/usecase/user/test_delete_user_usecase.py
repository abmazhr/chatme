from pytest import fixture

from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.usecase.user.delete_user import DeleteUserUseCase
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success
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
    delete_usecase = DeleteUserUseCase(
        config=None,
        persistence=db
    )

    created_domain_user = generate_valid_domain_user()
    add_usecase.execute(
        username=created_domain_user.name,
        age=created_domain_user.age,
        password=created_domain_user.password,
        email=created_domain_user.email,
        role=created_domain_user.role
    )

    yield add_usecase, delete_usecase, created_domain_user
    del add_usecase, delete_usecase, created_domain_user


def test_valid_delete_user(setup):
    add_usecase, delete_usecase, created_domain_user = setup
    add_usecase: AddUserUseCase
    delete_usecase: DeleteUserUseCase
    created_domain_user: DomainUser

    # by id
    assert isinstance(delete_usecase.execute(
        delete_by_selector="id",
        delete_by_data="0"
    ), Success)

    add_usecase.execute(
        username=created_domain_user.name,
        age=created_domain_user.age,
        password=created_domain_user.password,
        email=created_domain_user.email,
        role=created_domain_user.role
    )

    # by name
    assert isinstance(delete_usecase.execute(
        delete_by_selector="name",
        delete_by_data="test",
    ), Success)

    add_usecase.execute(
        username=created_domain_user.name,
        age=created_domain_user.age,
        password=created_domain_user.password,
        email=created_domain_user.email,
        role=created_domain_user.role
    )

    # by email
    assert isinstance(delete_usecase.execute(
        delete_by_selector="email",
        delete_by_data="test@test.com",
    ), Success)


def test_invalid_update_user(setup):
    _add_usecase, delete_usecase, created_domain_user = setup
    _add_usecase: AddUserUseCase
    delete_usecase: DeleteUserUseCase
    created_domain_user: DomainUser

    # by invalid selector
    assert delete_usecase.execute(
        delete_by_selector="invalid_selector",
        delete_by_data="invalid_data"
    ) == Failure(error="Delete selector should be within this list ['id', 'name', 'email']")

    # by id
    assert delete_usecase.execute(
        delete_by_selector="id",
        delete_by_data="invalid"
    ) == Failure(error='There is no user with id invalid to be deleted')

    # by name
    assert delete_usecase.execute(
        delete_by_selector="name",
        delete_by_data="invalid"
    ) == Failure(error='There is no user with name invalid to be deleted')

    # by email
    assert delete_usecase.execute(
        delete_by_selector="email",
        delete_by_data="invalid"
    ) == Failure(error='There is no user with email invalid to be deleted')
