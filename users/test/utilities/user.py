from src.domain.entity.user import create_user


def generate_valid_domain_user():
    return create_user(
        name="test",
        age=26,
        password="Str0ngPassword",
        email="test@test.com"
    )
