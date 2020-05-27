import marshmallow_dataclass

from src.domain.entity.user import UserRole
from src.application.types import (
    Maybe,
    Dict,
    Any,
    dataclass
)


@dataclass(frozen=True)
class UserJson:
    id: str
    name: str
    age: int
    email: Maybe[str]
    role: UserRole

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            id=self.id,
            name=self.name,
            age=self.age,
            email=self.email,
            role=self.role.name
        )


# compatibility with marshmallow serialization
# maybe making it better later ;)
marshmallow_dataclass.class_schema(UserJson)
