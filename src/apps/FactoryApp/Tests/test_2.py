import  pytest
from django.contrib.auth.models import User

def test_new_user(db, user_factory):
    user = user_factory.build()
    print(User.objects.count())
    print(user.username)
    assert True
