from src.application.types import (
    NamedTuple,
    Maybe
)


class DatabaseUser(NamedTuple):
    id: str
    name: str
    age: int
    email: Maybe[str]
    password: str
