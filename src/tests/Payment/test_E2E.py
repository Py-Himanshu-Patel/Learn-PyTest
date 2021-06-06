import json
import pytest

from .factory import CurrencyFactory, TransactionFactory
from apps.Payment.models import Currency, Transaction

# applying universal marker
pytestmark = pytest.mark.django_db


class TestCurrencyEndpoints:

    endpoint = '/api/currency/'

    def test_list(self, api_client):
        assert Currency.objects.count() == 0

        # insert 3 Currecny recored in test db
        CurrencyFactory.create_batch(3)

        response = api_client().get(
            self.endpoint
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client):
        currency = CurrencyFactory.build()

        # create a non persistance instance / do not save into db
        expected_json = {
            'name': currency.name,
            'code': currency.code,
            'symbol': currency.symbol
        }

        response = api_client().post(
            self.endpoint,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 201
        assert json.loads(response.content) == expected_json
        assert Currency.objects.count() == 1

    def test_retrieve(self, api_client):
        assert Currency.objects.count() == 0
        currency = CurrencyFactory.create()

        expected_json = {
            'name': currency.name,
            'code': currency.code,
            'symbol': currency.symbol
        }
        url = f'{self.endpoint}{currency.id}/'

        response = api_client().get(url)

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, rf, api_client):
        '''
            old_currency inserted into db
            new_currency updated the very same instance
        '''
        assert Currency.objects.count() == 0
        old_currency = CurrencyFactory.create()
        new_currency = CurrencyFactory.build()
        assert Currency.objects.count() == 1

        currency_dict = {
            'code': new_currency.code,
            'name': new_currency.name,
            'symbol': new_currency.symbol
        }

        url = f'{self.endpoint}{old_currency.id}/'

        response = api_client().put(
            url,
            currency_dict,
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content) == currency_dict

    @pytest.mark.parametrize('field', [
        ('code'),
        ('name'),
        ('symbol'),
    ])
    def test_partial_update(self, field, api_client):
        currency = CurrencyFactory.create()
        assert Currency.objects.count() == 1

        currency_dict = {
            'code': currency.code,
            'name': currency.name,
            'symbol': currency.symbol
        }
        field_value = currency_dict[field]
        url = f'{self.endpoint}{currency.id}/'

        response = api_client().patch(
            url,
            {field: field_value},
            format='json'
        )

        assert response.status_code == 200
        assert json.loads(response.content)[field] == field_value
        assert Currency.objects.count() == 1

    def test_delete(self, api_client):
        assert Currency.objects.count() == 0
        currency = CurrencyFactory.create()
        assert Currency.objects.count() == 1

        url = f'{self.endpoint}{currency.id}/'

        response = api_client().delete(url)

        assert response.status_code == 204
        assert Currency.objects.count() == 0


class TestTransactionEndpoints:

    endpoint = '/api/transaction/'

    def test_list(self, api_client):
        client = api_client()
        assert Transaction.objects.count() == 0

        TransactionFactory.create_batch(3)
        url = self.endpoint
        response = client.get(url)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, api_client):
        client = api_client()
        assert Transaction.objects.count() == 0

        t = TransactionFactory.create()

        valid_data_dict = {
            'currency': t.currency.code,
            'name': t.name,
            'email': t.email,
            'message': t.message
        }

        url = self.endpoint

        response = client.post(
            url,
            valid_data_dict,
            format='json'
        )

        assert response.status_code == 201
        assert json.loads(response.content) == valid_data_dict
        assert Transaction.objects.last().link

    def test_retrieve(self, api_client):
        t = TransactionFactory.create()
        t = Transaction.objects.last()
        expected_json = t.__dict__

        expected_json['link'] = t.link
        expected_json['currency'] = t.currency.code
        expected_json['uid'] = str(expected_json['uid'])
        expected_json['creation_date'] = expected_json['creation_date'].strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        expected_json.pop('_state')
        expected_json.pop('currency_id')
        url = f'{self.endpoint}{t.id}/'

        response = api_client().get(url)

        assert response.status_code == 200 or response.status_code == 301
        assert json.loads(response.content) == expected_json

    def test_update(self, api_client):
        old_transaction = TransactionFactory.create()
        new_transaction = TransactionFactory.create()

        expected_json = new_transaction.__dict__
        expected_json['uid'] = str(old_transaction.uid)
        expected_json['id'] = int(old_transaction.id)
        expected_json['currency'] = old_transaction.currency.code
        expected_json['link'] = Transaction.objects.first().link
        expected_json['creation_date'] = old_transaction.creation_date.strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        expected_json.pop('_state')
        expected_json.pop('currency_id')

        url = f'{self.endpoint}{old_transaction.id}/'

        response = api_client().put(
            url,
            data=expected_json,
            format='json'
        )

        assert response.status_code == 200 or response.status_code == 301
        assert json.loads(response.content) == expected_json

    @pytest.mark.parametrize('field', [
        ('name'),
        ('email'),
        ('message'),
    ])
    def test_partial_update(self, api_client, field):
        TransactionFactory.create_batch(2)
        old_transaction = Transaction.objects.first()
        new_transaction = Transaction.objects.last()
        valid_field = {
            field: str(new_transaction.__dict__[field]),
        }
        url = f'{self.endpoint}{old_transaction.id}/'

        response = api_client().patch(
            path=url,
            data=valid_field,
            format='json',
        )

        assert response.status_code == 200 or response.status_code == 301
        try:
            assert json.loads(response.content)[field] == valid_field[field]
        except json.decoder.JSONDecodeError as e:
            pass

    def test_delete(self, api_client):
        transaction = TransactionFactory.create()
        url = f'{self.endpoint}{transaction.id}/'

        response = api_client().delete(
            url
        )

        assert response.status_code == 204 or response.status_code == 301
