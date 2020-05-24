from pytest import fixture
from starlette.testclient import TestClient

from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.entity.user_json import UserJson
from src.application.infrastructure.web.rest_api.starlette import StarletteRestApi
from src.application.infrastructure.web.schema.json.user.post_user import post_user
from src.application.infrastructure.web.validation.jsonschema import JsonSchemaValidator
from src.application.usecase.user.add_user import AddUserUseCase
from src.domain.entity.user import DomainUser
from test.utilities.user import generate_valid_domain_user


@fixture(scope="function")
def setup():
    db = InMemoryDatabase(
        config=None
    )
    host = "0.0.0.0"
    port = 3000
    api = StarletteRestApi(
        config=None,
        host=host,
        port=port,
        routes=[
            Route(
                url="/users",
                methods=["POST"],
                handler=StarletteRestApi.post_user,
                args=None,
                kwargs=dict(
                    add_user_usecase=AddUserUseCase(
                        config=None,
                        persistence=db
                    ),
                    json_schema=post_user,
                    json_schema_validator=JsonSchemaValidator(
                        config=None
                    )
                )
            )
        ]
    )
    test_api = TestClient(app=api.__dict__["_StarletteRestApi__app"])

    yield test_api
    del api, test_api, db


def test_valid_add_user(setup):
    api = setup
    api: TestClient

    domain_user: DomainUser = generate_valid_domain_user()

    assert api.post(
        url="/users",
        json={
            "name": domain_user.name,
            "age": domain_user.age,
            "password": domain_user.password,
            "email": domain_user.email
        }
    ).json() == UserJson(id="0", name=domain_user.name, age=domain_user.age, email=domain_user.email).as_dict()

    assert api.post(
        url="/users",
        json={
            "name": domain_user.name,
            "age": domain_user.age,
            "password": domain_user.password,
            "email": domain_user.email
        }
    ).json() == {'error': 'Username test is already exist, please use a different name.'}


def test_invalid_add_user(setup):
    api = setup
    api: TestClient

    domain_user: DomainUser = generate_valid_domain_user()

    # invalid data
    assert api.post(
        url="/users",
        json={
            "password": domain_user.password,
            "email": domain_user.email
        }
    ).json() == {'error': "'name' is a required property"}

    # empty name
    assert api.post(
        url="/users",
        json={
            "name": "",
            "age": domain_user.age,
            "password": domain_user.password,
            "email": domain_user.email
        }
    ).json() == {
               'error': "name can't be empty.\n"
                        'name should be at least 2 characters.\n'
                        'name should be alpha or alpha numeric.'
           }

    # invalid age as string
    assert api.post(
        url="/users",
        json={
            "name": domain_user.name,
            "age": "invalid",
            "password": domain_user.password,
            "email": domain_user.email
        }
    ).json() == {'error': "'invalid' is not of type 'number'"}

    # weak password
    assert api.post(
        url="/users",
        json={
            "name": domain_user.name,
            "age": domain_user.age,
            "password": "weak_password",
            "email": domain_user.email
        }
    ).json() == {'error': 'password should be stronger.'}

    # invalid email
    assert api.post(
        url="/users",
        json={
            "name": domain_user.name,
            "age": domain_user.age,
            "password": domain_user.password,
            "email": "invalid_email"
        }
    ).json() == {'error': 'email should be a valid one.'}
