from src.application.infrastructure.web.entity.json import JsonEntity, _A
from src.application.types import (
    Maybe,
    NamedTuple,
    List,
    Tuple,
    Dict,
    Any,
    Callable
)


class Route(NamedTuple):
    url: str
    methods: List[str]
    handler: Callable[..., JsonEntity.of(_type=_A)]
    args: Maybe[Tuple[Any, ...]]
    kwargs: Maybe[Dict[str, Any]]
