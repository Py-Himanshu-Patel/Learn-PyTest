import  pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_new_user(user_factory):
	user = user_factory.create()
	print(User.objects.count())		# 1
	print(user.username)			# Cath Nelson
	assert True
