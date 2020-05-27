import os
import sys

from application.infrastructure.web.schema.json.user.login_user import login_user
from application.usecase.user.add_access_token import AddAccessTokenUseCase

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.application.entity.service import Service
from src.application.infrastructure.persistence.in_memory import InMemoryDatabase
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.rest_api.starlette import StarletteRestApi
from src.application.infrastructure.web.schema.json.user.post_user import post_user
from src.application.infrastructure.web.schema.json.user.put_user import put_user
from src.application.infrastructure.web.validation.jsonschema import JsonSchemaValidator
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.usecase.user.delete_user import DeleteUserUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.application.usecase.user.update_user import UpdateUserUseCase

db = InMemoryDatabase(config=None)

StarletteRestApi(
    config=None,
    host="0.0.0.0",
    port=3000,
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
        ),
        Route(
            url="/users",
            methods=["GET"],
            handler=StarletteRestApi.get_user,
            args=None,
            kwargs=dict(
                fetch_user_usecase=FetchUserUseCase(config=None, persistence=db)
            )
        ),
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
        ),
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
        ),
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
        ),
        Route(
            url="/healthz",
            methods=["GET"],
            handler=StarletteRestApi.health_check,
            args=None,
            kwargs=dict(
                services=[Service(service_instance=db)]
            )
        )
    ]
).run(host='0.0.0.0', port=3000, debug=False, workers=1)
