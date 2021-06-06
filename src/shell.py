# to run use: python manage.py shell < shell.py

from tests.Payment.factory import CurrencyFactory
from apps.Payment.models import Currency

print(Currency.objects.all())
print(Currency.objects.all().count())
print('----------------------')
# print(Currency.objects.all())
# c = CurrencyFactory.build()
for c in CurrencyFactory.create_batch(3):
	print(c.__dict__)

