from src.domain.entity.failure import Failure
from src.domain.entity.user import User


def test_valid_user_creation():
    name: str = "name"
    age: int = 26
    email: str = "email@test.com"
    password: str = "StrongPassw0rd"

    # alpha name
    assert User.create_user(
        name=name,
        age=age,
        password=password,
        email=email
    ) == User(
        name=name,
        age=age,
        email=email,
        password=password  # for now but later will be encrypted
    )

    # alpha numeric name
    assert User.create_user(
        name=name + "2",
        age=age,
        password=password,
        email=email
    ) == User(
        name=name + "2",
        age=age,
        email=email,
        password=password  # for now but later will be encrypted
    )


def test_invalid_user_creation():
    name: str = "name"
    age: int = 26
    email: str = "email@test.com"
    password: str = "StrongPassw0rd"

    # empty name
    assert User.create_user(
        name="",
        age=age,
        password=password,
        email=email
    ) == Failure(error="name can't be empty.\n"
                       "name should be at least 2 characters.\n"
                       "name should be alpha or alpha numeric.")

    # one char name
    assert User.create_user(
        name="a",
        age=age,
        password=password,
        email=email
    ) == Failure(error='name should be at least 2 characters.')

    # less than 16 age <just a number to have limit in the app :D>
    assert User.create_user(
        name=name,
        age=15,
        password=password,
        email=email
    ) == Failure(error='age should be between 16 and 150.')

    # more than 150 age <just a number to have limit in the app :D>
    assert User.create_user(
        name=name,
        age=151,
        password=password,
        email=email
    ) == Failure(error='age should be between 16 and 150.')

    # weak password
    assert User.create_user(
        name=name,
        age=26,
        password="weak",
        email=email
    ) == Failure(error='password should be stronger.')

    # invalid email
    assert User.create_user(
        name=name,
        age=26,
        password=password,
        email="invalid_email"
    ) == Failure(error='email should be a valid one.')
