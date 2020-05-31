from pytest import fixture
from starlette.testclient import TestClient

from src.application.infrastructure.web.entity.access_token import AccessToken
from src.application.infrastructure.web.schema.json.user.login_user import login_user
from src.application.usecase.user.add_access_token import AddAccessTokenUseCase
from src.application.usecase.user.fetch_access_token import FetchAccessTokenUseCase
from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.rest_api.framework_logic.starlette import StarletteRestApi
from src.application.infrastructure.web.validation.jsonschema import JsonSchemaValidator
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
                url="/users/login",
                methods=["POST"],
                handler=StarletteRestApi.get_access_token,
                args=None,
                kwargs=dict(
                    add_access_token_usecase=AddAccessTokenUseCase(
                        config=None,
                        persistence=db
                    ),
                    json_schema=login_user,
                    json_schema_validator=JsonSchemaValidator(
                        config=None
                    )
                )
            )
        ]
    )
    domain_user: DomainUser = generate_valid_domain_user()
    db.persist_user(user=domain_user)

    test_api = TestClient(app=api.__dict__["_StarletteRestApi__app"])

    yield test_api, domain_user, db
    del api, test_api, db


def test_valid_get_access_token(setup):
    api, domain_user, db = setup
    api: TestClient
    domain_user: DomainUser
    db: InMemoryDatabase

    access_token_json = api.post(
        url="/users/login",
        json={
            "username": domain_user.name,
            "password": domain_user.password,
        }
    ).json()

    assert access_token_json["token"] is not None

    assert isinstance(FetchAccessTokenUseCase(
        config=None,
        persistence=db
    ).execute(
        username=domain_user.name
    ), AccessToken)


def test_invalid_get_access_token(setup):
    api, domain_user, _db = setup
    api: TestClient
    domain_user: DomainUser
    _db: InMemoryDatabase

    assert api.post(
        url="/users/login",
        json={
            "username": "invalid_username",
            "password": domain_user.password,
        }
    ).json() == {'error': 'There is no user with name invalid_username to be fetched'}
