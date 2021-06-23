from logging import exception
import factory
import pytest

from apps.Payment.serializers import CurrencySerializer, UnfilledTransactionSerializer, FilledTransactionSerializer
from tests.Payment.factory import CurrencyFactory, TransactionFactory, FilledTransactionFactory


class TestCurrencySerializer:
    @pytest.mark.unit
    def test_serialize_model(self):
        currency = CurrencyFactory.build()
        serializer = CurrencySerializer(currency)
        assert serializer.data

    @pytest.mark.unit
    def test_serialized_data(self):
        # returns a dict containing data of model instance
        valid_serializer_data = factory.build(
            dict,
            FACTORY_CLASS=CurrencyFactory
        )

        serializer = CurrencySerializer(data=valid_serializer_data)
        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}


class TestUnfilledTransactionSerializer:
    
    @pytest.mark.unit
    def test_serialize_model(self):
        transaction = TransactionFactory.build()
        expected_serialized_data = {
            'name': transaction.name,
            'currency': transaction.currency.code,
            'email': transaction.email,
            'message': transaction.message,
        }

        serializer = UnfilledTransactionSerializer(transaction)
        assert serializer.data == expected_serialized_data

    # its a integration test as I can't do it without accessing DB
    @pytest.mark.django_db
    def test_serialized_data(self):
        # although the obj of Transaction is not saved in DB but
        # but instance of Currency is save to which transaction refers
        c = CurrencyFactory()
        transaction = TransactionFactory.build(currency=c)

        valid_serialized_data = {
            'name': transaction.name,
            'currency': transaction.currency.code,
            'email': transaction.email,
            'message': transaction.message,
        }

        serializer = UnfilledTransactionSerializer(data=valid_serialized_data)
        
        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}


class TestFilledTransactionSerializer:

    @pytest.mark.unit
    def test_serializer_model(self):
        transaction = FilledTransactionFactory.build()
        serializer = FilledTransactionSerializer(transaction)

        expected_data = {
            'id': transaction.id,
            'currency': str(transaction.currency),
            'link': transaction.link,
            'uid': str(transaction.uid),
            'name': transaction.name,
            'email': transaction.email,
            'creation_date': transaction.creation_date,
            'payment_intent_id': transaction.payment_intent_id,
            'message': transaction.message
        }

        assert serializer.data == expected_data

    @pytest.mark.unit
    def test_serializer_data(self):
        transaction = FilledTransactionFactory.build()

        validated_data = {
            'id': transaction.id,
            'currency': str(transaction.currency),
            'link': transaction.link,
            'uid': str(transaction.uid),
            'name': transaction.name,
            'email': transaction.email,
            'creation_date': transaction.creation_date,
            'payment_intent_id': transaction.payment_intent_id,
            'message': transaction.message
        }

        serializer = FilledTransactionSerializer(data=validated_data)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}
