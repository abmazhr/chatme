from pytest import fixture
from starlette.testclient import TestClient

from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.entity.user_json import UserJson
from src.application.infrastructure.web.rest_api.starlette import StarletteRestApi
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.domain.entity.user import DomainUser
from test.utilities.user import generate_valid_domain_user


@fixture(scope="function")
def setup():
    db = InMemoryDatabase(
        config=None
    )
    domain_user = generate_valid_domain_user()
    db.persist_user(user=domain_user)

    api = StarletteRestApi(
        config=None,
        routes=[
            Route(
                url="/users",
                methods=["GET"],
                handler=StarletteRestApi.get_user,
                args=None,
                kwargs=dict(
                    fetch_user_usecase=FetchUserUseCase(
                        config=None,
                        persistence=db
                    ),
                )
            )
        ]
    )
    test_api = TestClient(app=api.__dict__["_StarletteRestApi__app"])

    yield test_api, domain_user
    del api, test_api, db


def test_valid_get_user(setup):
    api, domain_user = setup
    api: TestClient
    domain_user: DomainUser

    user_json = UserJson(id="0", name=domain_user.name, age=domain_user.age, email=domain_user.email)._asdict()

    dummy_id = "0"
    assert api.get(
        url=f"/users?id={dummy_id}"
    ).json() == user_json

    dummy_name = domain_user.name
    assert api.get(
        url=f"/users?name={dummy_name}"
    ).json() == user_json

    dummy_email = domain_user.email
    assert api.get(
        url=f"/users?email={dummy_email}"
    ).json() == user_json


def test_invalid_get_user(setup):
    api, domain_user = setup
    api: TestClient
    domain_user: DomainUser

    # empty id
    dummy_id = ""
    assert api.get(
        url=f"/users?id={dummy_id}"
    ).json() == {'error': 'There is no user with id  to be fetched'}

    # empty name
    dummy_name = ""
    assert api.get(
        url=f"/users?name={dummy_name}"
    ).json() == {'error': 'There is no user with name  to be fetched'}

    # empty email
    dummy_email = ""
    assert api.get(
        url=f"/users?email={dummy_email}"
    ).json() == {'error': 'There is no user with email  to be fetched'}

    # by age
    dummy_age = domain_user.age
    assert api.get(
        url=f"/users?age={dummy_age}"
    ).json() == {'error': "Fetch selector should be within this list ['id', 'name', 'email']"}
