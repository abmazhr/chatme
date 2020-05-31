from pytest import fixture
from starlette.testclient import TestClient

from src.application.entity.health_check import Status
from src.application.entity.service import Service
from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.rest_api.framework_logic.starlette import StarletteRestApi


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
                url="/health",
                methods=["GET"],
                handler=StarletteRestApi.health_check,
                args=None,
                kwargs=dict(services=[
                    Service(
                        service_instance=db
                    )
                ])
            )
        ]
    )
    test_api = TestClient(app=api.__dict__["_StarletteRestApi__app"])

    yield test_api, db
    del api, test_api


def test_valid_health_check(setup):
    api, db = setup
    api: TestClient
    db: InMemoryDatabase

    assert api.get(
        url="/health"
    ).json() == {db.__class__.__name__: Status.HEALTHY.name}
