import factory
from django.contrib.auth.models import User
from faker import Faker
fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	# specifing some default args to user model
	username = fake.name()
	is_staff = True
