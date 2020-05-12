from src.application.entity.user import ApplicationUser
from src.application.infrastructure.persistence import PersistenceInterface
from src.domain.entity.user import create_user, DomainUser


def test_from_domain_user_to_application_user():
    domain_user: DomainUser = create_user(
        name="test",
        age=26,
        password="Str0ngPassword",
        email="test@test.com"
    )
    assert PersistenceInterface.from_domain_user_to_database_user(
        user=domain_user,
        user_id="0"
    ) == ApplicationUser(
        id="0",
        name=domain_user.name,
        age=domain_user.age,
        email=domain_user.email,
        password=domain_user.password
    )


def test_from_application_user_to_domain_user():
    application_user: ApplicationUser = ApplicationUser(
        id="0",
        name="test",
        age=26,
        password="Str0ngPassword",
        email="test@test.com"
    )
    assert PersistenceInterface.from_database_user_to_domain_user(
        user=application_user,
    ) == DomainUser(
        name=application_user.name,
        age=application_user.age,
        email=application_user.email,
        password=application_user.password
    )
