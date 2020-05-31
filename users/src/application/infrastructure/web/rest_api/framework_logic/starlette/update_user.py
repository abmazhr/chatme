from starlette.requests import Request
from starlette.responses import JSONResponse

from src.application.entity.user import ApplicationUser
from src.application.infrastructure.web.entity.json import JsonEntity, _A
from src.application.infrastructure.web.validation import JsonValidatorInterface
from src.application.types import (
    Dict,
    Any,
    Callable,
    Either
)
from src.application.usecase.user.fetch_access_token import FetchAccessTokenUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.application.usecase.user.update_user import UpdateUserUseCase
from src.application.utilities.user import from_application_user_to_json_user
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success
from src.domain.entity.user import create_user, UserRole


async def update_user(*,
                      update_user_usecase: UpdateUserUseCase,
                      fetch_user_usecase: FetchUserUseCase,
                      fetch_access_token_usecase: FetchAccessTokenUseCase,
                      json_schema: Dict[str, Any],
                      json_schema_validator: JsonValidatorInterface,
                      request: Request) -> Callable[..., JsonEntity.of(_type=_A)]:
    # simple validation for now, will be better later ;)
    username = request.headers.get("username", None)
    token = request.headers.get("access-token", None)
    if username is not None and token is not None:
        current_logged_user_fetch_status = fetch_user_usecase.execute(
            fetch_by_selector='name',
            fetch_by_data=username
        )
        access_token_status = fetch_access_token_usecase.execute(
            username=username
        )
        if isinstance(access_token_status, Failure):
            return JSONResponse(access_token_status.as_dict(), 401)

        if access_token_status.token != token:
            return JSONResponse(Failure(error=f"Invalid access token for the user {username}").as_dict(), 401)

        if isinstance(current_logged_user_fetch_status, ApplicationUser):
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
                if current_logged_user_fetch_status.role.name == UserRole.ADMIN.name:
                    pass
                elif current_logged_user_fetch_status.role.name == UserRole.USER.name:
                    if current_logged_user_fetch_status.name != username:
                        return JSONResponse(
                            Failure(
                                error="Your current user permission is not satisfying this operation."
                            ).as_dict(),
                            status_code=401
                        )

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

        return JSONResponse(current_logged_user_fetch_status.as_dict(), 401)

    return JSONResponse(
        Failure(error="You should provide username and access-token into the headers.").as_dict(), 401
    )
