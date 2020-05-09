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
email_pattern: Pattern[AnyStr] = compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
password_pattern: Pattern[AnyStr] = compile(r"^(?=.{8,32}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*")


class User(NamedTuple):
    name: str
    age: int
    password: str
    email: Maybe[str]

    @staticmethod
    def create_user(*,
                    name: str,
                    age: int,
                    password: str,
                    email: Maybe[str]) -> Either[Failure, 'User']:
        # simple validation
        results: List[Either[Failure, Success]] = [
            User.__validate(field=field, err_msg=err_msg, func=func)
            # maybe making this in a better container class later to make it looks easier ;)
            for field, err_msg, func in (
                (name, "name can't be empty.",
                 lambda _name: _name != ""),
                (name, "name should be at least 2 characters.",
                 lambda _name: len(_name) >= 2),
                (name, "name should be alpha or alpha numeric.",
                 lambda _name: str.isalpha(_name) or str.isalnum(_name)),
                (age, "age should be between 16 and 150.",
                 lambda _age: 150 >= age >= 16),
                (email, "email should be a valid one.",
                 lambda _email: _email is None or email_pattern.match(_email)),
                (password, "password can't be empty.",
                 lambda _password: _password != ""),
                (password, "password should be stronger.",
                 lambda _password: password_pattern.match(_password)),
            )
        ]
        failures: List[Failure] = list(filter(lambda ins: isinstance(ins, Failure), results))

        return User(
            name=name,
            age=age,
            password=password,
            email=email
        ) if len(failures) == 0 else Failure(error="\n".join(list(map(lambda failure: failure.error, failures))))

    @staticmethod
    def __validate(*,
                   field: Any,
                   err_msg: str,
                   func: Callable[[Any], bool]) -> Either[Failure, Success]:
        return Success() if func(field) else Failure(error=err_msg)
