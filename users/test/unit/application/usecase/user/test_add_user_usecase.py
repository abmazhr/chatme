from pytest import fixture

from src.application.infrastructure.persistence import PersistenceInterface
from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.usecase.user.add_user import AddUserUseCase
from src.domain.entity.failure import Failure
from src.domain.entity.user import DomainUser, UserRole
from test.utilities.user import generate_valid_domain_user


@fixture(scope='function')
def setup():
    usecase = AddUserUseCase(
        config=None,
        persistence=InMemoryDatabase(
            config=None
        )
    )
    yield usecase
    del usecase


def test_valid_add_user(setup):
    generated_domain_user: DomainUser = generate_valid_domain_user()

    usecase: AddUserUseCase = setup
    # other variety of valid data is covered on the user_tests itself
    assert usecase.execute(
        username=generated_domain_user.name,
        age=generated_domain_user.age,
        password=generated_domain_user.password,
        email=generated_domain_user.email,
        role=generated_domain_user.role
    ) == PersistenceInterface.from_domain_user_to_database_user(
        user=generated_domain_user,
        user_id="0"
    )


def test_invalid_add_user(setup):
    name = "test"
    age = 26
    password = "weak_password"
    email = "test@test.com"
    role = UserRole.USER

    usecase: AddUserUseCase = setup
    # other variety of invalid data is covered on the user_tests itself
    assert usecase.execute(
        username=name,
        age=age,
        password=password,
        email=email,
        role=role
    ) == Failure(error='password should be stronger.')
