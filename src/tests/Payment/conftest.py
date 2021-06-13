import pytest
from .factory import TransactionFactory, CurrencyFactory
from pytest_factoryboy import register

register(CurrencyFactory)
register(TransactionFactory)


@pytest.fixture
def create_currency(db, currency_factory):
    currency = currency_factory.create()
    return currency

@pytest.fixture
def build_currency(db, currency_factory):
    currency = currency_factory.build()
    return currency

@pytest.fixture
def create_transaction(db, transaction_factory):
    transaction = transaction_factory.create()
    return transaction

@pytest.fixture
def get_payment_id():
    return "tnMMv6"
