import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_create1():
	User.objects.create_user(
		username='test',
		email='test@email.com',
		password='abcd@1234'
	)
	count = User.objects.count()
	print(count)
	assert  count == 1


@pytest.mark.django_db
def test_user_create2():
	count = User.objects.count()
	print(count)
	assert  count == 0	
