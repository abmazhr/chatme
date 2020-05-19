from jsonschema import validate

from src.application.infrastructure.web.validation import JsonValidatorInterface
from src.application.types import (
    Any,
    Dict,
    SimpleConfig,
    Maybe,
    Either
)
from src.application.utilities.functions import exception_handler
from src.domain.entity.failure import Failure
from src.domain.entity.success import Success


class JsonSchemaValidator(JsonValidatorInterface):
    def __init__(self, *, config: Maybe[SimpleConfig]) -> None:
        super().__init__(config=config)

    @exception_handler
    def validate(self, *,
                 schema: Dict[str, Any],
                 data: Dict[str, Any]) -> Either[Failure, Success]:
        validate(
            schema=schema,
            instance=data
        )
        return Success()
