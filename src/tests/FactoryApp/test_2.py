import pytest
from django.contrib.auth.models import User


def test_new_user(create_user):
    user = create_user
    print(User.objects.count())  # 1
    print(user.username)        # django
    assert True
