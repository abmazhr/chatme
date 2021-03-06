from src.domain.entity.failure import Failure
from src.domain.entity.user import DomainUser, create_user, UserRole


def test_valid_user_creation():
    name: str = "name"
    age: int = 26
    email: str = "email@test.com"
    password: str = "StrongPassw0rd"

    # alpha name
    assert create_user(
        name=name,
        age=age,
        password=password,
        email=email,
        role=UserRole.USER
    ) == DomainUser(
        name=name,
        age=age,
        email=email,
        password=password,  # for now but later will be encrypted
        role=UserRole.USER
    )

    # alpha numeric name
    assert create_user(
        name=name + "2",
        age=age,
        password=password,
        email=email,
        role=UserRole.USER
    ) == DomainUser(
        name=name + "2",
        age=age,
        email=email,
        password=password,  # for now but later will be encrypted
        role=UserRole.USER
    )


def test_invalid_user_creation():
    name: str = "name"
    age: int = 26
    email: str = "email@test.com"
    password: str = "StrongPassw0rd"

    # empty name
    assert create_user(
        name="",
        age=age,
        password=password,
        email=email,
        role=UserRole.USER
    ) == Failure(error="name can't be empty.\n"
                       "name should be at least 2 characters.\n"
                       "name should be alpha or alpha numeric.")

    # one char name
    assert create_user(
        name="a",
        age=age,
        password=password,
        email=email,
        role=UserRole.USER
    ) == Failure(error='name should be at least 2 characters.')

    # less than 16 age <just a number to have limit in the app :D>
    assert create_user(
        name=name,
        age=15,
        password=password,
        email=email,
        role=UserRole.USER
    ) == Failure(error='age should be between 16 and 150.')

    # more than 150 age <just a number to have limit in the app :D>
    assert create_user(
        name=name,
        age=151,
        password=password,
        email=email,
        role=UserRole.USER
    ) == Failure(error='age should be between 16 and 150.')

    # weak password
    assert create_user(
        name=name,
        age=26,
        password="weak",
        email=email,
        role=UserRole.USER
    ) == Failure(error='password should be stronger.')

    # invalid email
    assert create_user(
        name=name,
        age=26,
        password=password,
        email="invalid_email",
        role=UserRole.USER
    ) == Failure(error='email should be a valid one.')
