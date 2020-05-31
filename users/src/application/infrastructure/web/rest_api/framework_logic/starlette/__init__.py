import os
from typing import Callable, List

import marshmallow_dataclass
import uvicorn
import yaml
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_apispec import APISpecSchemaGenerator
from swagger_ui import api_doc

from src.application.entity.service import Service
from src.application.infrastructure.web.entity.json import JsonEntity, _A
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.rest_api import RestApiInterface
from src.application.infrastructure.web.rest_api.common_logic.health_check import health_check as health_check_common
from src.application.infrastructure.web.rest_api.framework_logic.starlette.delete_user import (
    delete_user as delete_user_framework
)
from src.application.infrastructure.web.rest_api.framework_logic.starlette.get_access_token import (
    get_access_token as get_access_token_framework
)
from src.application.infrastructure.web.rest_api.framework_logic.starlette.get_user import (
    get_user as get_user_framework
)
from src.application.infrastructure.web.rest_api.framework_logic.starlette.post_user import (
    post_user as post_user_framework
)
from src.application.infrastructure.web.rest_api.framework_logic.starlette.update_user import (
    update_user as update_user_framework
)
from src.application.infrastructure.web.validation import JsonValidatorInterface
from src.application.types import (
    Maybe,
    Dict,
    Any,
    SimpleConfig,
    dataclass
)
from src.application.usecase.user.add_access_token import AddAccessTokenUseCase
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.usecase.user.delete_user import DeleteUserUseCase
from src.application.usecase.user.fetch_access_token import FetchAccessTokenUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.application.usecase.user.update_user import UpdateUserUseCase
from src.application.utilities.functions import exception_handler
from src.domain.entity.user import DomainUser


class StarletteRestApi(RestApiInterface):
    def __init__(self, *,
                 config: Maybe[SimpleConfig],
                 host: str,
                 port: int,
                 routes: List[Route]) -> None:
        self.__app = Starlette()
        self.__open_api_schema = APISpecSchemaGenerator(
            APISpec(
                title="Users Service API",
                version="1.0",
                openapi_version="3.0.0",
                info={"description": "This is the generated API docs of the users service"},
                plugins=[MarshmallowPlugin()]
            )
        )
        super().__init__(config=config, host=host, port=port, routes=routes)

    def register_generated_openid_docs(self, *, host: str, port: int) -> None:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        schema_yaml_file_name = 'open_api.yaml'
        schema_yaml_file_path = os.path.join(cur_dir, f'./{schema_yaml_file_name}')

        self.__app.add_route(
            path="/schema",
            route=self.open_api_schema(),
            methods=["GET", "HEAD"],
            include_in_schema=False
        )

        @exception_handler
        @self.__app.on_event("shutdown")
        def shutdown() -> None:
            os.remove(schema_yaml_file_path)

        yaml_open_api_schema = yaml.dump(
            self.__open_api_schema.get_schema(routes=self.__app.routes),
            default_flow_style=False
        )

        with open(schema_yaml_file_path, 'w') as writer:
            writer.write("servers:\n"
                         f"- url: http://{host}:{port}\n")
            writer.write(yaml_open_api_schema)

        api_doc(self.__app, config_path=schema_yaml_file_path, url_prefix="/swagger.io/docs")

    def open_api_schema(self) -> Callable[..., Any]:
        async def wrapper(request: Request) -> Any:
            return self.__open_api_schema.OpenAPIResponse(request=request)

        return wrapper

    def register_endpoints(self, *, routes: List[Route]) -> None:
        def get_proper_handler_args(_route: Route) -> Route.handler:
            return (
                _route.handler() if _route.args is None and _route.kwargs is None
                else _route.handler(*_route.args) if _route.args is not None and _route.kwargs is None
                else _route.handler(**_route.kwargs) if _route.args is None and _route.kwargs is not None
                else _route.handler(*_route.args, **_route.kwargs)
            )

        for route in routes:
            self.__app.add_route(
                path=route.url,
                methods=route.methods,
                route=get_proper_handler_args(_route=route)
            )

    @classmethod
    def health_check(cls, *, services: List[Service]) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(_request: Request) -> JSONResponse:
            """
            responses:
                200:
                    description: health check of all services
                    examples:
                        - {"InMemoryDatabase": "HEALTHY"}
                        - {"InMemoryDatabase": "UNHEALTHY"}
            """
            return JSONResponse(health_check_common(services=services))

        return wrapper

    @classmethod
    def get_access_token(cls, *,
                         add_access_token_usecase: AddAccessTokenUseCase,
                         json_schema: Dict[str, Any],
                         json_schema_validator: JsonValidatorInterface) -> Callable[..., JsonEntity.of(_type=_A)]:
        @dataclass(frozen=True)
        class UserLoginJson:
            username: str
            password: str

        marshmallow_dataclass.class_schema(UserLoginJson)

        async def wrapper(request: Request) -> JSONResponse:
            """
            requestBody:
                description: Data to login a user and generate an access token for this particular user
                required: true
                content:
                  application/json:
                    schema: UserLoginJson
            responses:
                200:
                    description: AccessToken created
                    content:
                        application/json:
                            schema: AccessToken
                    examples:
                        - {"token": "token"}
                400:
                    description: error generating an access token
                    content:
                        application/json:
                            schema: Failure
                    examples:
                    - {"error": "Invalid password for this user"}
            """
            json_data: Dict[Any, Any] = await request.json()
            return await get_access_token_framework(
                add_access_token_usecase=add_access_token_usecase,
                json_schema=json_schema,
                json_schema_validator=json_schema_validator,
                json_data=json_data
            )

        return wrapper

    @classmethod
    def post_user(cls, *,
                  add_user_usecase: AddUserUseCase,
                  json_schema: Dict[str, Any],
                  json_schema_validator: JsonValidatorInterface) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(request: Request) -> JSONResponse:
            """
            requestBody:
                description: Data to create a user
                required: true
                content:
                  application/json:
                    schema: DomainUser
            responses:
                200:
                    description: User created
                    content:
                        application/json:
                            schema: UserJson
                    examples:
                        - {"name": "test", "age": 26, "email": "test@test.com", "role": "USER"}
                400:
                    description: error creating a user
                    content:
                        application/json:
                            schema: Failure
                    examples:
                    - {"error": "Username string is already exist, please use a different name."}
            """
            json_data: Dict[Any, Any] = await request.json()
            return await post_user_framework(
                add_user_usecase=add_user_usecase,
                json_schema=json_schema,
                json_schema_validator=json_schema_validator,
                json_data=json_data
            )

        return wrapper

    @classmethod
    def get_user(cls, *,
                 fetch_user_usecase: FetchUserUseCase,
                 fetch_access_token_usecase: FetchAccessTokenUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(request: Request) -> JSONResponse:
            """
            parameters:
                - in: header
                  name: username
                  schema:
                    type: string
                  description: The username of the user who has an access-token
                  require: true
                - in: header
                  name: access-token
                  schema:
                    type: string
                  description: The access-token of the user currently doing this request
                  require: true
                - in: query
                  name: id
                  schema:
                    type: string
                  description: The id of the user
                - in: query
                  name: name
                  schema:
                    type: string
                  description: The name of the user
                - in: query
                  name: email
                  schema:
                    type: string
                  description: The email of the user
            responses:
             200:
               description: the user you fetched
               content:
                    application/json:
                        schema: UserJson
               examples:
                   - {"name": "test", "age": 26, "email": "test@test.com", "role": "USER"}
             400:
               description: error fetching the user
               content:
                    application/json:
                        schema: Failure
               examples:
                   - {"error": "You should provide params as one of these [id, name, email]"}
             401:
                description: unauthorized
                content:
                    application/json:
                        schema: Failure
                examples:
                    - {"error": "You should provide username and access-token into the headers."}
            """
            return await get_user_framework(
                fetch_user_usecase=fetch_user_usecase,
                fetch_access_token_usecase=fetch_access_token_usecase,
                request=request
            )

        return wrapper

    @classmethod
    def update_user(cls, *,
                    update_user_usecase: UpdateUserUseCase,
                    fetch_user_usecase: FetchUserUseCase,
                    fetch_access_token_usecase: FetchAccessTokenUseCase,
                    json_schema: Dict[str, Any],
                    json_schema_validator: JsonValidatorInterface) -> Callable[..., JsonEntity.of(_type=_A)]:
        @dataclass(frozen=True)
        class UpdateUserData:
            update_by_selector: str
            update_by_data: str
            updated_user: DomainUser

        marshmallow_dataclass.class_schema(UpdateUserData)

        async def wrapper(request: Request) -> JSONResponse:
            """
            parameters:
                - in: header
                  name: username
                  schema:
                    type: string
                  description: The username of the user who has an access-token
                  require: true
                - in: header
                  name: access-token
                  schema:
                    type: string
                  description: The access-token of the user currently doing this request
                  require: true
            requestBody:
                description: Data to update a user
                required: true
                content:
                  application/json:
                    schema: UpdateUserData
            responses:
                200:
                    description: User updated
                    content:
                        application/json:
                            schema: ApplicationUser
                    examples:
                        - {"name": "test", "age": 26, "email": "test@test.com", "password": "Str0ngPassword", "role": "USER"}
                400:
                    description: Error updating the user
                    content:
                        application/json:
                            schema: Failure
                    examples:
                    - {"error": "Update selector should be within this list ['id', 'name', 'email']"}
                401:
                    description: unauthorized
                    content:
                        application/json:
                            schema: Failure
                    examples:
                        - {"error": "You should provide username and access-token into the headers."}
            """
            return await update_user_framework(
                update_user_usecase=update_user_usecase,
                fetch_user_usecase=fetch_user_usecase,
                fetch_access_token_usecase=fetch_access_token_usecase,
                json_schema=json_schema,
                json_schema_validator=json_schema_validator,
                request=request
            )

        return wrapper

    @classmethod
    def delete_user(cls, *,
                    delete_user_usecase: DeleteUserUseCase,
                    fetch_user_usecase: FetchUserUseCase,
                    fetch_access_token_usecase: FetchAccessTokenUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(request: Request) -> JSONResponse:
            """
            parameters:
                - in: header
                  name: username
                  schema:
                    type: string
                  description: The username of the user who has an access-token
                  require: true
                - in: header
                  name: access-token
                  schema:
                    type: string
                  description: The access-token of the user currently doing this request
                  require: true
                - in: query
                  name: id
                  schema:
                    type: string
                  description: The id of the user
                - in: query
                  name: name
                  schema:
                    type: string
                  description: The name of the user
                - in: query
                  name: email
                  schema:
                    type: string
                  description: The email of the user
            responses:
                200:
                    description: User deleted
                400:
                    description: Error deleting the user
                    content:
                        application/json:
                            schema: Failure
                    examples:
                    - {"error": "Delete selector should be within this list ['id', 'name', 'email']"}
                401:
                    description: unauthorized
                    content:
                        application/json:
                            schema: Failure
                    examples:
                        - {"error": "You should provide username and access-token into the headers."}
            """
            return await delete_user_framework(
                delete_user_usecase=delete_user_usecase,
                fetch_user_usecase=fetch_user_usecase,
                fetch_access_token_usecase=fetch_access_token_usecase,
                request=request
            )

        return wrapper

    def run(self, *, host: str, port: int, debug: bool, workers: int) -> None:
        print(f"SERVICE-API documentation can be found on http://{host}:{port}/swagger.io/docs")
        uvicorn.run(
            self.__app,
            host=host,
            port=port,
            debug=debug
        )
