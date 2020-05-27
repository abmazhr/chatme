import marshmallow_dataclass

from src.domain.entity.user import UserRole
from src.application.types import (
    Maybe,
    dataclass,
    Dict,
    Any
)


@dataclass(frozen=True)
class ApplicationUser:
    id: str
    name: str
    age: int
    email: Maybe[str]
    password: str
    role: UserRole

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            id=self.id,
            name=self.name,
            age=self.age,
            email=self.email,
            password=self.password,
            role=self.role.name
        )


# compatibility with marshmallow serialization
# maybe making it better later ;)
marshmallow_dataclass.class_schema(ApplicationUser)
