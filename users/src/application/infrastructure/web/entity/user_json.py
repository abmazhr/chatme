from src.application.types import (
    NamedTuple,
    Maybe
)


class UserJson(NamedTuple):
    id: str
    name: str
    age: int
    email: Maybe[str]
