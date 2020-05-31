from starlette.responses import JSONResponse

from src.application.infrastructure.web.entity.access_token import AccessToken
from src.application.infrastructure.web.entity.json import JsonEntity, _A
from src.application.infrastructure.web.validation import JsonValidatorInterface
from src.application.types import (
    Dict,
    Any,
    Callable,
    Either
)
from src.application.usecase.user.add_access_token import AddAccessTokenUseCase
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success


async def get_access_token(*,
                           add_access_token_usecase: AddAccessTokenUseCase,
                           json_schema: Dict[str, Any],
                           json_schema_validator: JsonValidatorInterface,
                           json_data: Dict[Any, Any]) -> Callable[..., JsonEntity.of(_type=_A)]:
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
