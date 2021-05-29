import pytest
from django.contrib.auth.models import User

@pytest.fixture
def create_user(db):
    return User.objects.create_user(
        username='test',
        email='test@email.com'
    )

def test_set_check_password(create_user):
    create_user.set_password('new-password')
    assert create_user.check_password('new-password') == True

