from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.Payment.models import Transaction
from apps.Payment.utils import fill_transaction


@receiver(post_save, sender=Transaction)
def transaction_filler(sender, instance, created, *args, **kwargs):
	''' fill 'payment_intent_id' field in a transacton before saving '''

	if created:
		fill_transaction(instance)
