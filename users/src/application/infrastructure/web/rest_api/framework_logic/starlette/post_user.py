from starlette.responses import JSONResponse

from src.application.entity.user import ApplicationUser
from src.application.infrastructure.web.entity.json import JsonEntity, _A
from src.application.infrastructure.web.entity.user_json import UserJson
from src.application.infrastructure.web.validation import JsonValidatorInterface
from src.application.types import (
    Dict,
    Any,
    Callable,
    Either
)
from src.application.usecase.user.add_user import AddUserUseCase
from src.application.utilities.user import from_application_user_to_json_user
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success
from src.domain.entity.user import UserRole


async def post_user(*,
                    add_user_usecase: AddUserUseCase,
                    json_schema: Dict[str, Any],
                    json_schema_validator: JsonValidatorInterface,
                    json_data: Dict[Any, Any]) -> Callable[..., JsonEntity.of(_type=_A)]:
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
