from src.application.entity.user import ApplicationUser
from src.application.infrastructure.web.entity.user_json import UserJson


def from_application_user_to_json_user(*, application_user: ApplicationUser) -> UserJson:
    return UserJson(
        id=application_user.id,
        name=application_user.name,
        age=application_user.age,
        email=application_user.email
    )
