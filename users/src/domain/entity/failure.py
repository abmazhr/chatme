import marshmallow_dataclass

from src.domain.types import dataclass, Dict


@dataclass(frozen=True)
class Failure:
    error: str

    def as_dict(self) -> Dict[str, str]:
        return dict(
            error=self.error
        )


# compatibility with marshmallow serialization
# maybe making it better later ;)
marshmallow_dataclass.class_schema(Failure)
