from re import compile

from src.domain.entity.failure import Failure
from src.domain.entity.success import Success
from src.domain.types import (
    Any,
    Maybe,
    Either,
    Callable,
    NamedTuple,
    Pattern,
    AnyStr,
    List
)

# simple regex for now ;)
__email_pattern: Pattern[AnyStr] = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
__password_pattern: Pattern[AnyStr] = compile(r"^(?=.{8,32}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*")


class User(NamedTuple):
    name: str
    age: int
    password: str
    email: Maybe[str]


class __VContainer(NamedTuple):
    field: Any
    err_msg: str
    func: Callable[[Any], bool]


def create_user(*,
                name: str,
                age: int,
                password: str,
                email: Maybe[str]) -> Either[Failure, User]:
    # simple validation
    results: List[Either[Failure, Success]] = list(map(
        __validate, (
            __VContainer(
                field=name,
                err_msg="name can't be empty.",
                func=lambda _name: _name != ""
            ),
            __VContainer(
                field=name,
                err_msg="name should be at least 2 characters.",
                func=lambda _name: len(_name) >= 2
            ),
            __VContainer(
                field=name,
                err_msg="name should be alpha or alpha numeric.",
                func=lambda _name: str.isalpha(_name) or str.isalnum(_name)
            ),
            __VContainer(
                field=age,
                err_msg="age should be between 16 and 150.",
                func=lambda _age: 150 >= age >= 16
            ),
            __VContainer(
                field=email,
                err_msg="email should be a valid one.",
                func=lambda _email: _email is None or __email_pattern.match(_email)
            ),
            __VContainer(
                field=password,
                err_msg="password can't be empty.",
                func=lambda _password: _password != ""
            ),
            __VContainer(
                field=password,
                err_msg="password should be stronger.",
                func=lambda _password: __password_pattern.match(_password) is not None
            ),
        )))

    failures: List[Failure] = list(filter(lambda ins: isinstance(ins, Failure), results))

    return User(
        name=name,
        age=age,
        password=password,
        email=email
    ) if len(failures) == 0 else Failure(error="\n".join(list(map(lambda failure: failure.error, failures))))


def __validate(vcontainer: __VContainer) -> Either[Failure, Success]:
    return Success() if vcontainer.func(vcontainer.field) else Failure(error=vcontainer.err_msg)
