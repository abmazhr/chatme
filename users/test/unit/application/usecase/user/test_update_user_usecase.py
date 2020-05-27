from pytest import fixture

from src.application.entity.user import ApplicationUser
from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.usecase.user.update_user import UpdateUserUseCase
from src.domain.entity.failure import Failure
from src.domain.entity.user import DomainUser as DomainUser
from src.domain.entity.user import create_user
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
    update_usecase = UpdateUserUseCase(
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

    yield update_usecase, created_domain_user
    del add_usecase, update_usecase, created_domain_user


def test_valid_update_user(setup):
    usecase, created_domain_user = setup
    usecase: UpdateUserUseCase
    created_domain_user: DomainUser

    updated_domain_user: DomainUser = create_user(
        name="newname",
        age=created_domain_user.age + 10,
        password=created_domain_user.password,
        email=created_domain_user.email,
        role=created_domain_user.role
    )

    # by id
    assert usecase.execute(
        update_by_selector="id",
        update_by_data="0",
        updated_user=updated_domain_user
    ) == ApplicationUser(
        id="0",
        name=updated_domain_user.name,
        age=updated_domain_user.age,
        email=updated_domain_user.email,
        password=updated_domain_user.password,
        role=updated_domain_user.role
    )

    # by name
    assert usecase.execute(
        update_by_selector="name",
        update_by_data="test",
        updated_user=updated_domain_user
    ) == ApplicationUser(
        id="0",
        name=updated_domain_user.name,
        age=updated_domain_user.age,
        email=updated_domain_user.email,
        password=updated_domain_user.password,
        role=updated_domain_user.role
    )

    # by email
    assert usecase.execute(
        update_by_selector="email",
        update_by_data="test@test.com",
        updated_user=updated_domain_user
    ) == ApplicationUser(
        id="0",
        name=updated_domain_user.name,
        age=updated_domain_user.age,
        email=updated_domain_user.email,
        password=updated_domain_user.password,
        role=updated_domain_user.role
    )


def test_invalid_update_user(setup):
    usecase, created_domain_user = setup
    usecase: UpdateUserUseCase
    created_domain_user: DomainUser

    updated_domain_user: DomainUser = create_user(
        name="newname",
        age=created_domain_user.age + 10,
        password=created_domain_user.password,
        email=created_domain_user.email,
        role=created_domain_user.role
    )

    # by invalid selector
    assert usecase.execute(
        update_by_selector="invalid_selector",
        update_by_data="invalid_data",
        updated_user=updated_domain_user
    ) == Failure(error="Update selector should be within this list ['id', 'name', 'email']")

    # by id
    assert usecase.execute(
        update_by_selector="id",
        update_by_data="invalid",
        updated_user=updated_domain_user
    ) == Failure(error='There is no user with id invalid to be updated')

    # by name
    assert usecase.execute(
        update_by_selector="name",
        update_by_data="invalid",
        updated_user=updated_domain_user
    ) == Failure(error='There is no user with name invalid to be updated')

    # by email
    assert usecase.execute(
        update_by_selector="email",
        update_by_data="invalid",
        updated_user=updated_domain_user
    ) == Failure(error='There is no user with email invalid to be updated')
