import pytest
from django.contrib.auth.models import User


@pytest.fixture()
def create_user(db):
    user = User.objects.create_user(
        username='test',
        email='test@email.com'
    )
    print('Creating User')
    return user


@pytest.fixture()
def new_user_factory(db):
    # inner function
    def create_app_user(
        username: str,
        password: str = None,
        first_name: str = "firstname",
        last_name: str = "lastname",
        email: str = "user@email.com",
        is_staff: bool = False,
        is_superuser: bool = False,
        is_active: bool = True
    ):
        user = User.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active
        )
        return user
    return create_app_user

# include db as we need to access database


@pytest.fixture
def create_new_user(db, new_user_factory):
    return new_user_factory(
        'Test User',
        'password',
        'user_firstname',
        is_staff=True
    )
