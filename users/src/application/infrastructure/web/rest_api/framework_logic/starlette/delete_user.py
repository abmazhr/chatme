from starlette.requests import Request
from starlette.responses import JSONResponse

from src.application.entity.user import ApplicationUser
from src.application.infrastructure.web.entity.json import JsonEntity, _A
from src.application.types import (
    Callable
)
from src.application.usecase.user.delete_user import DeleteUserUseCase
from src.application.usecase.user.fetch_access_token import FetchAccessTokenUseCase
from src.application.usecase.user.fetch_user import FetchUserUseCase
from src.domain.entity.failure import Failure
from src.domain.entity.user import UserRole


async def delete_user(*,
                delete_user_usecase: DeleteUserUseCase,
                fetch_user_usecase: FetchUserUseCase,
                fetch_access_token_usecase: FetchAccessTokenUseCase,
                request: Request) -> Callable[..., JsonEntity.of(_type=_A)]:
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
                if current_logged_user_fetch_status.role.name == UserRole.ADMIN.name:
                    pass
                elif current_logged_user_fetch_status.role.name == UserRole.USER.name:
                    permission_error_json = JSONResponse(
                        Failure(
                            error="Your current user permission is not satisfying this operation."
                        ).as_dict(),
                        status_code=401
                    )

                    if selector_key == "id":
                        if current_logged_user_fetch_status.id != selector_value:
                            return permission_error_json
                    if selector_key == "name":
                        if current_logged_user_fetch_status.name != selector_value:
                            return permission_error_json
                    if selector_key == "email":
                        if current_logged_user_fetch_status.email != selector_value:
                            return permission_error_json

                delete_user_status = delete_user_usecase.execute(
                    delete_by_selector=selector_key,
                    delete_by_data=selector_value
                )

                return JSONResponse(delete_user_status.as_dict(), status_code=200)

            return JSONResponse(
                Failure(error="You should provide params as one of these [id, name, email]").as_dict(),
                status_code=400
            )

        return JSONResponse(current_logged_user_fetch_status.as_dict(), 401)
    return JSONResponse(
        Failure(error="You should provide username and access-token into the headers.").as_dict(), 401
    )
