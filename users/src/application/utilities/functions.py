from jsonschema import ValidationError

from src.application.types import (
    Callable,
    Any,
    Either
)
from src.domain.entity.failure import Failure


def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    def __wrapper(*args, **kwargs) -> Either[Failure, Any]:
        try:
            return func(*args, **kwargs)
        except ValidationError as ex:
            return Failure(error=str(ex).split("\n")[0].strip())
        except Exception as ex:
            return Failure(error=str(ex))

    return __wrapper
