from starlette.requests import Request
from starlette.responses import JSONResponse

from src.application.entity.user import ApplicationUser
from src.application.infrastructure.web.entity.json import JsonEntity, _A
from src.application.infrastructure.web.entity.user_json import UserJson
from src.application.types import (
    Callable
)
from src.application.usecase.user.fetch_access_token import FetchAccessTokenUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.application.utilities.user import from_application_user_to_json_user
from src.domain.entity.failure import Failure
from src.domain.entity.user import UserRole


async def get_user(*,
                   fetch_user_usecase: FetchUserUseCase,
                   fetch_access_token_usecase: FetchAccessTokenUseCase,
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
            params = request.query_params
            if len(params) > 0:
                selector_key = list(params.keys())[0]
                selector_value = params[selector_key]
                fetch_user_status = fetch_user_usecase.execute(
                    fetch_by_selector=selector_key,
                    fetch_by_data=selector_value
                )
                if isinstance(fetch_user_status, ApplicationUser):
                    if current_logged_user_fetch_status.role.name == UserRole.ADMIN.name:
                        pass
                    elif current_logged_user_fetch_status.role.name == UserRole.USER.name:
                        if fetch_user_status.name != username:
                            return JSONResponse(
                                Failure(
                                    error="Your current user permission is not satisfying this operation."
                                ),
                                status_code=401
                            )
                    user_json: UserJson = from_application_user_to_json_user(
                        application_user=fetch_user_status
                    )
                    return JSONResponse(user_json.as_dict(), status_code=200)

                return JSONResponse(fetch_user_status.as_dict(), status_code=400)
            return JSONResponse(
                Failure(error="You should provide params as one of these [id, name, email]").as_dict(),
                status_code=400
            )

        return JSONResponse(current_logged_user_fetch_status.as_dict(), 400)

    return JSONResponse(
        Failure(error="You should provide username and access-token into the headers.").as_dict(), 401
    )
