from src.application.utilities.functions import exception_handler
from src.domain.entity.failure import Failure


def test_valid_exception_handling_utility():
    @exception_handler
    def hello(name: str) -> str:
        return f"hello {name}."

    assert hello("test") == f"hello test."


def test_invalid_exception_handling_utility():
    @exception_handler
    def hello(_name: str) -> str:
        raise Exception("Boom !")

    assert hello("test") == Failure(error='Boom !')
