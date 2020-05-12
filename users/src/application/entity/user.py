from src.application.types import (
    NamedTuple,
    Maybe
)


class ApplicationUser(NamedTuple):
    id: str
    name: str
    age: int
    email: Maybe[str]
    password: str
