from .factory import TransactionFactory
from apps.Payment.utils import Stripe
from apps.Payment.models import Transaction
from apps.Payment.utils import fill_transaction


class TestUtilFunctions:

    def test_fill_transaction(self, mocker, get_payment_id):

        transaction = TransactionFactory.build()
        strip_intent_id = get_payment_id

        # mocking API call
        payment_intent_mock = mocker.Mock(return_value=strip_intent_id)
        Stripe.create = payment_intent_mock

        # mocking DB calls
        filter_call_mock = mocker.Mock()
        Transaction.objects.filter = filter_call_mock
        update_call_mock = mocker.Mock()
        filter_call_mock.return_value.update = update_call_mock

        # call the function to be tested
        fill_transaction(transaction)

        filter_call_mock.assert_called_with(id=transaction.id)
        update_call_mock.assert_called_with(
            payment_intent_id=strip_intent_id
        )
