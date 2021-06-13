import string
import random


class Stripe:
    # to represent a call to strip API
    @staticmethod
    def create(length):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))


def fill_transaction(transaction):
    # get a transaction id before making an transaction
    payment_intent_id = Stripe.create(6)

    # get the queryset of all those transaction with this id
    t = transaction.__class__.objects.filter(id=transaction.id)

    # We use update not to trigger a save-signal recursion Overflow
    t.update(
        payment_intent_id=payment_intent_id,
    )
