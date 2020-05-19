from typing import Callable, List

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.application.entity.service import Service
from src.application.entity.user import ApplicationUser
from src.application.infrastructure.web.entity.json import JsonEntity, _A
from src.application.infrastructure.web.entity.route import Route
from src.application.infrastructure.web.rest_api import RestApiInterface
from src.application.infrastructure.web.validation import JsonValidatorInterface
from src.application.types import (
    Maybe,
    Either,
    Dict,
    Any,
    SimpleConfig
)
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.usecase.user.delete_user import DeleteUserUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.application.usecase.user.update_user import UpdateUserUseCase
from src.application.utilities.user import from_application_user_to_json_user
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success
from src.domain.entity.user import create_user


class StarletteRestApi(RestApiInterface):
    def __init__(self, *, config: Maybe[SimpleConfig], routes: List[Route]) -> None:
        self.__app = Starlette()
        super().__init__(config=config, routes=routes)

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
            def get_service_health_status(service):
                try:
                    return service.service_instance.health_check().service_state.name
                except Exception:
                    return f"There is no 'health_check' function for this service " \
                           f"[{service.service_instance.__class__.__name__}]."

            return JSONResponse({
                service.service_instance.__class__.__name__: get_service_health_status(service)
                for service in services
            })

        return wrapper

    @classmethod
    def post_user(cls, *,
                  add_user_usecase: AddUserUseCase,
                  json_schema: Dict[str, Any],
                  json_schema_validator: JsonValidatorInterface) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(request: Request) -> JSONResponse:
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
                    email=json_data.get("email", None)
                )
                if isinstance(add_user_status, ApplicationUser):
                    return JSONResponse(from_application_user_to_json_user(
                        application_user=add_user_status
                    )._asdict())

                return JSONResponse(add_user_status._asdict())
            return JSONResponse(json_validation_status._asdict())

        return wrapper

    @classmethod
    def get_user(cls, *, fetch_user_usecase: FetchUserUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(request: Request) -> JSONResponse:
            params = request.query_params

            selector_key = list(params.keys())[0]
            selector_value = params[selector_key]
            fetch_user_status = fetch_user_usecase.execute(
                fetch_by_selector=selector_key,
                fetch_by_data=selector_value
            )

            if isinstance(fetch_user_status, ApplicationUser):
                return JSONResponse(from_application_user_to_json_user(
                    application_user=fetch_user_status
                )._asdict())

            return JSONResponse(fetch_user_status._asdict())

        return wrapper

    @classmethod
    def update_user(cls, *,
                    update_user_usecase: UpdateUserUseCase,
                    json_schema: Dict[str, Any],
                    json_schema_validator: JsonValidatorInterface) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(request: Request) -> JSONResponse:
            json_data: Dict[Any, Any] = await request.json()
            json_validation_status: Either[Failure, Success] = json_schema_validator.validate(
                schema=json_schema,
                data=json_data
            )
            if isinstance(json_validation_status, Success):
                create_domain_user_status = create_user(
                    **json_data["updated_user"]
                )
                if isinstance(create_domain_user_status, Failure):
                    return JSONResponse(create_domain_user_status._asdict())

                update_user_status = update_user_usecase.execute(
                    update_by_selector=json_data["update_by_selector"],
                    update_by_data=json_data["update_by_data"],
                    updated_user=create_domain_user_status
                )
                if isinstance(update_user_status, ApplicationUser):
                    return JSONResponse(from_application_user_to_json_user(
                        application_user=update_user_status
                    )._asdict())

                return JSONResponse(update_user_status._asdict())
            return JSONResponse(json_validation_status._asdict())

        return wrapper

    @classmethod
    def delete_user(cls, *, delete_user_usecase: DeleteUserUseCase) -> Callable[..., JsonEntity.of(_type=_A)]:
        async def wrapper(request: Request) -> JSONResponse:
            params = request.query_params

            selector_key = list(params.keys())[0]
            selector_value = params[selector_key]
            delete_user_status = delete_user_usecase.execute(
                delete_by_selector=selector_key,
                delete_by_data=selector_value
            )

            return JSONResponse(delete_user_status._asdict())

        return wrapper

    def run(self, *, host: str, port: int, debug: bool, workers: int) -> None:
        uvicorn.run(
            self.__app,
            host=host,
            port=port,
            debug=debug
        )
