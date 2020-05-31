from pytest import fixture
from starlette.testclient import TestClient

from src.application.infrastructure.web.rest_api.framework_logic.starlette import StarletteRestApi
from src.application.infrastructure.web.entity.access_token import AccessToken
from src.application.usecase.user.fetch_access_token import FetchAccessTokenUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.infrastructure.web.entity.route import Route
from src.application.usecase.user.delete_user import DeleteUserUseCase
from src.domain.entity.success import Success
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
                methods=["DELETE"],
                handler=StarletteRestApi.delete_user,
                args=None,
                kwargs=dict(
                    delete_user_usecase=DeleteUserUseCase(
                        config=None,
                        persistence=db
                    ),
                    fetch_user_usecase=FetchUserUseCase(
                        config=None,
                        persistence=db
                    ),
                    fetch_access_token_usecase=FetchAccessTokenUseCase(
                        config=None,
                        persistence=db
                    )
                )
            )
        ]
    )
    test_api = TestClient(app=api.__dict__["_StarletteRestApi__app"])

    yield test_api, db
    del api, test_api, db


def test_valid_delete_user(setup):
    api, db = setup
    api: TestClient
    db: InMemoryDatabase

    domain_user = generate_valid_domain_user()
    db.persist_user(user=domain_user)
    token: AccessToken = db.persist_access_token(username=domain_user.name, password=domain_user.password)

    # by id
    db.persist_user(user=domain_user)
    dummy_id = "0"
    assert api.delete(
        url=f"/users?id={dummy_id}",
        headers={
            'username': domain_user.name,
            'access-token': token.token
        }
    ).json() == Success().as_dict()

    # by name
    db.persist_user(user=domain_user)
    dummy_name = domain_user.name
    assert api.delete(
        url=f"/users?name={dummy_name}",
        headers={
            'username': domain_user.name,
            'access-token': token.token
        }
    ).json() == Success().as_dict()

    # by email
    db.persist_user(user=domain_user)
    dummy_email = domain_user.email
    assert api.delete(
        url=f"/users?email={dummy_email}",
        headers={
            'username': domain_user.name,
            'access-token': token.token
        }
    ).json() == Success().as_dict()


def test_invalid_delete_user(setup):
    api, db = setup
    api: TestClient
    db: InMemoryDatabase

    domain_user = generate_valid_domain_user()

    # empty headers
    db.persist_user(user=domain_user)
    token: AccessToken = db.persist_access_token(username=domain_user.name, password=domain_user.password)
    dummy_id = 200
    assert api.delete(
        url=f"/users?id={dummy_id}",
        headers={
            'username': domain_user.name,
            'access-token': "invalid"
        }
    ).json() == {'error': 'Invalid access token for the user test'}

    # invalid user
    db.persist_user(user=domain_user)
    token: AccessToken = db.persist_access_token(username=domain_user.name, password=domain_user.password)
    dummy_id = 200
    assert api.delete(
        url=f"/users?id={dummy_id}",
        headers={
            'username': "invaliduser",
            'access-token': token.token
        }
    ).json() == {'error': 'There is no access token for user invaliduser'}

    # insufficient user permission
    db.persist_user(user=domain_user)
    token: AccessToken = db.persist_access_token(username=domain_user.name, password=domain_user.password)
    dummy_id = 200
    assert api.delete(
        url=f"/users?id={dummy_id}",
        headers={
            'username': domain_user.name,
            'access-token': token.token
        }
    ).json() == {'error': 'Your current user permission is not satisfying this operation.'}

    # invalid tokens
    db.persist_user(user=domain_user)
    token: AccessToken = db.persist_access_token(username=domain_user.name, password=domain_user.password)
    dummy_id = 200
    assert api.delete(
        url=f"/users?id={dummy_id}",
    ).json() == {'error': 'You should provide username and access-token into the headers.'}

    # invalid id
    db.persist_user(user=domain_user)
    token: AccessToken = db.persist_access_token(username=domain_user.name, password=domain_user.password)
    dummy_id = 200
    assert api.delete(
        url=f"/users?id={dummy_id}",
        headers={
            'username': domain_user.name,
            'access-token': token.token
        }
    ).json() == {'error': 'Your current user permission is not satisfying this operation.'}

    # invalid name
    db.persist_user(user=domain_user)
    dummy_name = "invalid"
    assert api.delete(
        url=f"/users?name={dummy_name}",
        headers={
            'username': domain_user.name,
            'access-token': token.token
        }
    ).json() == {'error': 'Your current user permission is not satisfying this operation.'}

    # invalid age selector
    db.persist_user(user=domain_user)
    dummy_age = domain_user.age
    assert api.delete(
        url=f"/users?age={dummy_age}",
        headers={
            'username': domain_user.name,
            'access-token': token.token
        }
    ).json() == {'error': "Delete selector should be within this list ['id', 'name', 'email']"}
