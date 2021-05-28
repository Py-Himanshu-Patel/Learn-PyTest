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
