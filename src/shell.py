# to run use: python manage.py shell < shell.py

import factory
from faker import Faker
fake = Faker()
from apps.Payment.models import Currency


class CurrencyFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Currency
	name, code = fake.currency()

CurrencyFactory()
