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

from src.application.infrastructure.web.entity.access_token import AccessToken
from src.application.usecase.user.add_access_token import AddAccessTokenUseCase
from src.application.entity.service import Service
from src.application.entity.user import ApplicationUser
from src.application.infrastructure.web.entity.json import JsonEntity, _A
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.entity.user_json import UserJson
from src.application.infrastructure.web.rest_api import RestApiInterface
from src.application.infrastructure.web.validation import JsonValidatorInterface
from src.application.types import (
    Maybe,
    Either,
    Dict,
    Any,
    SimpleConfig,
    dataclass
)
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.usecase.user.delete_user import DeleteUserUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.application.usecase.user.update_user import UpdateUserUseCase
from src.application.utilities.functions import exception_handler
from src.application.utilities.user import from_application_user_to_json_user
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success
from src.domain.entity.user import create_user, DomainUser, UserRole


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

            def get_service_health_status(service):
                try:
                    return service.service_instance.health_check().service_state.name
                except Exception:
                    return f"There is no 'health_check' function for this service " \
                           f"[{service.service_instance.__class__.__name__}]."

            return JSONResponse({
                service.service_instance.__class__.__name__: get_service_health_status(service)
                for service in services
            }, status_code=200)

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
            json_validation_status: Either[Failure, Success] = json_schema_validator.validate(
                schema=json_schema,
                data=json_data
            )
            if isinstance(json_validation_status, Success):
                add_access_token_status = add_access_token_usecase.execute(
                    username=json_data["username"],
                    password=json_data["password"],
                )
                if isinstance(add_access_token_status, AccessToken):
                    return JSONResponse(add_access_token_status.as_dict(), status_code=200)

                return JSONResponse(add_access_token_status.as_dict(), status_code=400)
            return JSONResponse(json_validation_status.as_dict(), status_code=400)

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
            json_validation_status: Either[Failure, Success] = json_schema_validator.validate(
                schema=json_schema,
                data=json_data
            )
            if isinstance(json_validation_status, Success):
                add_user_status = add_user_usecase.execute(
                    username=json_data["name"],
                    age=json_data["age"],
                    password=json_data["password"],
                    email=json_data.get("email", None),
                    role=UserRole.USER
                )
                if isinstance(add_user_status, ApplicationUser):
                    user_json: UserJson = from_application_user_to_json_user(
                        application_user=add_user_status
                    )
                    return JSONResponse(user_json.as_dict(), status_code=200)

                return JSONResponse(add_user_status.as_dict(), status_code=400)
            return JSONResponse(json_validation_status.as_dict(), status_code=400)

        return wrapper

    @classmethod
    def get_user(cls, *, fetch_user_usecase: FetchUserUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(request: Request) -> JSONResponse:
            """
            parameters:
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
            """
            params = request.query_params

            if len(params) > 0:
                selector_key = list(params.keys())[0]
                selector_value = params[selector_key]
                fetch_user_status = fetch_user_usecase.execute(
                    fetch_by_selector=selector_key,
                    fetch_by_data=selector_value
                )

                if isinstance(fetch_user_status, ApplicationUser):
                    user_json: UserJson = from_application_user_to_json_user(
                        application_user=fetch_user_status
                    )
                    return JSONResponse(user_json.as_dict(), status_code=200)

                return JSONResponse(fetch_user_status.as_dict(), status_code=400)
            return JSONResponse(
                Failure(error="You should provide params as one of these [id, name, email]").as_dict(),
                status_code=400
            )

        return wrapper

    @classmethod
    def update_user(cls, *,
                    update_user_usecase: UpdateUserUseCase,
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
            """
            json_data: Dict[Any, Any] = await request.json()
            json_validation_status: Either[Failure, Success] = json_schema_validator.validate(
                schema=json_schema,
                data=json_data
            )
            if isinstance(json_validation_status, Success):
                # will make this better later ;)
                json_data["updated_user"]["role"] = UserRole.USER
                create_domain_user_status = create_user(
                    **json_data["updated_user"]
                )
                if isinstance(create_domain_user_status, Failure):
                    return JSONResponse(create_domain_user_status.as_dict())

                update_user_status = update_user_usecase.execute(
                    update_by_selector=json_data["update_by_selector"],
                    update_by_data=json_data["update_by_data"],
                    updated_user=create_domain_user_status
                )
                if isinstance(update_user_status, ApplicationUser):
                    user_json = from_application_user_to_json_user(
                        application_user=update_user_status
                    )
                    return JSONResponse(user_json.as_dict(), status_code=200)

                return JSONResponse(update_user_status.as_dict(), status_code=400)
            return JSONResponse(json_validation_status.as_dict(), status_code=400)

        return wrapper

    @classmethod
    def delete_user(cls, *, delete_user_usecase: DeleteUserUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(request: Request) -> JSONResponse:
            """
            parameters:
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
            """
            params = request.query_params

            if len(params) > 0:
                selector_key = list(params.keys())[0]
                selector_value = params[selector_key]
                delete_user_status = delete_user_usecase.execute(
                    delete_by_selector=selector_key,
                    delete_by_data=selector_value
                )

                return JSONResponse(delete_user_status.as_dict(), status_code=200)

            return JSONResponse(
                Failure(error="You should provide params as one of these [id, name, email]").as_dict(),
                status_code=400
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
