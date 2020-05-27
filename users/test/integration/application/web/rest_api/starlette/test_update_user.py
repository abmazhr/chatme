from pytest import fixture
from starlette.testclient import TestClient

from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.entity.user_json import UserJson
from src.application.infrastructure.web.rest_api.starlette import StarletteRestApi
from src.application.infrastructure.web.schema.json.user.put_user import put_user
from src.application.infrastructure.web.validation.jsonschema import JsonSchemaValidator
from src.application.usecase.user.update_user import UpdateUserUseCase
from src.domain.entity.user import DomainUser, create_user
from test.utilities.user import generate_valid_domain_user


@fixture(scope="function")
def setup():
    db = InMemoryDatabase(
        config=None
    )
    domain_user = generate_valid_domain_user()
    db.persist_user(user=domain_user)
    host = "0.0.0.0"
    port = 3000

    api = StarletteRestApi(
        config=None,
        host=host,
        port=port,
        routes=[
            Route(
                url="/users",
                methods=["PUT"],
                handler=StarletteRestApi.update_user,
                args=None,
                kwargs=dict(
                    update_user_usecase=UpdateUserUseCase(
                        config=None,
                        persistence=db
                    ),
                    json_schema=put_user,
                    json_schema_validator=JsonSchemaValidator(
                        config=None
                    )
                )
            )
        ]
    )
    test_api = TestClient(app=api.__dict__["_StarletteRestApi__app"])

    yield test_api, domain_user
    del api, test_api, db


def test_valid_update_user(setup):
    api, domain_user = setup
    api: TestClient
    domain_user: DomainUser

    updated_domain_user = create_user(
        name="newname",
        age=domain_user.age,
        email=domain_user.email,
        password=domain_user.password,
        role=domain_user.role
    )

    updated_user_json = UserJson(
        id="0",
        name=updated_domain_user.name,
        age=updated_domain_user.age,
        email=updated_domain_user.email,
        role=updated_domain_user.role
    ).as_dict()

    dummy_id = "0"
    assert api.put(
        url="/users",
        json={
            'updated_user': updated_domain_user.as_dict(),
            'update_by_selector': 'id',
            'update_by_data': dummy_id
        }
    ).json() == updated_user_json


def test_invalid_update_user(setup):
    api, domain_user = setup
    api: TestClient
    domain_user: DomainUser

    dummy_id = "0"

    # invalid data
    assert api.put(
        url="/users",
        json={
            'updated_user': dict(
                name="new_name",
                age=domain_user.age,
                email=domain_user.email,
                password=domain_user.password
            ),
        }
    ).json() == {'error': "'update_by_selector' is a required property"}

    # invalid new name
    assert api.put(
        url="/users",
        json={
            'updated_user': dict(
                name="new_name",
                age=domain_user.age,
                email=domain_user.email,
                password=domain_user.password
            ),
            'update_by_selector': 'id',
            'update_by_data': dummy_id
        }
    ).json() == {'error': 'name should be alpha or alpha numeric.'}

    # invalid age
    assert api.put(
        url="/users",
        json={
            'updated_user': dict(
                name=domain_user.name,
                age=200,
                email=domain_user.email,
                password=domain_user.password
            ),
            'update_by_selector': 'id',
            'update_by_data': dummy_id
        }
    ).json() == {'error': 'age should be between 16 and 150.'}

    # invalid email
    assert api.put(
        url="/users",
        json={
            'updated_user': dict(
                name=domain_user.name,
                age=domain_user.age,
                email="invalid_email",
                password=domain_user.password
            ),
            'update_by_selector': 'id',
            'update_by_data': dummy_id
        }
    ).json() == {'error': 'email should be a valid one.'}
