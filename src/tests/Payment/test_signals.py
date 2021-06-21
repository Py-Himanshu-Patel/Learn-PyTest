import pytest

from django.db.models.signals import post_save

from apps.Payment.models import Transaction
from tests.Payment.factory import TransactionFactory


pytestmark = pytest.mark.unit

class TestTransactionFiller:

    def test_post_save(self, mocker):
        instance = TransactionFactory.build()
        mock = mocker.patch(
            'apps.Payment.signals.fill_transaction'
        )

        post_save.send(Transaction, instance=instance, created=True)
        mock.assert_called_with(instance)
