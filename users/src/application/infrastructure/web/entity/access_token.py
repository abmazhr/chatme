import marshmallow_dataclass

from src.application.types import dataclass, Dict


@dataclass(frozen=True)
class AccessToken:
    token: str

    def as_dict(self) -> Dict[str, str]:
        return dict(
            token=self.token
        )


# compatibility with marshmallow validation
# maybe making it better later ;)
marshmallow_dataclass.class_schema(AccessToken)
