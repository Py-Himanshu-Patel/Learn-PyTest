import pytest
from django.contrib.auth.models import User

@pytest.fixture
def create_user(db):
    user = User.objects.create_user(
        username='test',
        email='test@email.com'
    )
    print('Creating User')
    return user

def test_set_check_password1(create_user):
    print("Set Password 1")
    create_user.set_password('new-password1')
    assert create_user.check_password('new-password1') == True

def test_set_check_password2(create_user):
    print("Set Password 2")
    create_user.set_password('new-password2')
    assert create_user.check_password('new-password2') == True
