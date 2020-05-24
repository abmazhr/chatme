from pytest import fixture
from starlette.testclient import TestClient

from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.rest_api.starlette import StarletteRestApi
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

    # by id
    db.persist_user(user=domain_user)
    dummy_id = "0"
    assert api.delete(
        url=f"/users?id={dummy_id}",
    ).json() == Success().as_dict()

    # by name
    db.persist_user(user=domain_user)
    dummy_name = domain_user.name
    assert api.delete(
        url=f"/users?name={dummy_name}",
    ).json() == Success().as_dict()

    # by email
    db.persist_user(user=domain_user)
    dummy_email = domain_user.email
    assert api.delete(
        url=f"/users?email={dummy_email}",
    ).json() == Success().as_dict()


def test_invalid_delete_user(setup):
    api, db = setup
    api: TestClient
    db: InMemoryDatabase

    domain_user = generate_valid_domain_user()

    # invalid id
    db.persist_user(user=domain_user)
    dummy_id = 200
    assert api.delete(
        url=f"/users?id={dummy_id}"
    ).json() == {'error': 'There is no user with id 200 to be deleted'}

    # invalid name
    db.persist_user(user=domain_user)
    dummy_name = "invalid"
    assert api.delete(
        url=f"/users?name={dummy_name}"
    ).json() == {'error': 'There is no user with name invalid to be deleted'}

    # invalid age selector
    db.persist_user(user=domain_user)
    dummy_age = domain_user.age
    assert api.delete(
        url=f"/users?age={dummy_age}"
    ).json() == {'error': "Delete selector should be within this list ['id', 'name', 'email']"}
