# to run use: python manage.py shell < shell.py

from tests.Payment.factory import TransactionFactory
from apps.Payment.models import Transaction

print(Transaction.objects.all())
print(Transaction.objects.all().count())
print('----------------------')

for t in TransactionFactory.create_batch(3):
	print(t.__dict__)
	print()
