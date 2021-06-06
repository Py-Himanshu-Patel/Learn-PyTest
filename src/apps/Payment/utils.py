import string
import random


def strip_dummy_api(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def fill_transaction(transaction):
    # get a dummy transaction id before making an transaction
    payment_intent_id = strip_dummy_api(6)

    # get the queryset of all those transaction with this id 
    t = transaction.__class__.objects.filter(id=transaction.id)

    # We use update not to trigger a save-signal recursion Overflow
    t.update(  
        payment_intent_id=payment_intent_id,
    )
