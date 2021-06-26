import json

import pytest
from apps.Payment.models import Currency, Transaction
from apps.Payment.views import CurrencyViewSet, TransactionViewset
from django.urls import reverse
from django_mock_queries.mocks import MockSet
from rest_framework.relations import SlugRelatedField, StringRelatedField
from tests.Payment.factory import (CurrencyFactory,
                                   CurrencylessTransactionFactory,
                                   FilledTransactionFactory)

import factory

class TransactionInstanceToJson:
    @staticmethod
    def convert(transaction):
        ''' return the dict attribute of instance '''
        json_data = transaction.__dict__.copy()
        json_data['link'] = transaction.link
        json_data['uid'] = str(transaction.uid)
        json_data['currency'] = transaction.currency.code
        json_data.pop('_state')
        json_data.pop('currency_id')
        return json_data


class TestCurrencyViewset:

    def test_list(self, mocker, rf):
        '''
            mocker: is the tool in pytest to mock the attributes of class
            rf: request factory
        '''
        # Arrange
        # get the url based on url name
        url = reverse('currency-list')	# '/api/currency/'
        request = rf.get(url)			# <WSGIRequest: GET '/api/currency/'>
        
        # Mock
        # MockSet is a lib which provide a mocked obj just like queryset
        qs = MockSet(
            CurrencyFactory.build(),	# gives instance of Currency
            CurrencyFactory.build(),
            CurrencyFactory.build()
        )

        # make a get list request on view
        view = CurrencyViewSet.as_view(
            {'get': 'list'}
        )

        # mocking the get_queryset method 
        mocker.patch.object(
            CurrencyViewSet, 'get_queryset', return_value=qs
        )

        # Act
        # <Response status_code=200, "text/html; charset=utf-8">
        response = view(request).render()		

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, mocker, rf):
        # NO id assigned until the obj is save in DB
        currency = CurrencyFactory.build()
        expected_json = {
            'name': currency.name,
            'code': currency.code,
            'symbol': currency.symbol
        }

        # /api/currency/None/
        url = reverse('currency-detail', kwargs={'pk': currency.id})
        # <WSGIRequest: GET '/api/currency/None/'>
        request = rf.get(url)

        mocker.patch.object(
            CurrencyViewSet, 'get_queryset', return_value=MockSet(currency)
        )

        view = CurrencyViewSet.as_view(
            {'get': 'retrieve'}
        )

        # <Response status_code=200, "application/json">
        response = view(request, pk=currency.id).render()

        assert response.status_code == 200
        # {'name': 'Iranian rial', 'code': 'IRR', 'symbol': '$'}
        assert json.loads(response.content) == expected_json

    def test_create(self, mocker, rf):
        # {'code': 'CVE', 'name': 'Cape Verdean escudo', 'symbol': '$'} 
        valid_data_dict = factory.build(
            dict,
            FACTORY_CLASS=CurrencyFactory
        )

        # /api/currency/
        url = reverse('currency-list')

        # <WSGIRequest: POST '/api/currency/'>
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(valid_data_dict)
        )

        # Currency.save() = <MagicMock name='save()' id='2183017755552'>
        # in case of no return_value specified it returns MagicMock obj
        mocker.patch.object(
            Currency, 'save'
        )

        view = CurrencyViewSet.as_view(
            {'post': 'create'}
        )

        response = view(request).render()

        assert response.status_code == 201
        # response.content = b'{"name":"Cape Verdean escudo","code":"CVE","symbol":"$"}
        assert json.loads(response.content) == valid_data_dict

    def test_udpate(self, mocker, rf):
        old_currency = CurrencyFactory.build()
        new_currency = CurrencyFactory.build()

        # {'code': 'MKD', 'name': 'Macedonian denar', 'symbol': '$'}
        currency_dict = {
            'code': new_currency.code,
            'name': new_currency.name,
            'symbol': new_currency.symbol
        }

        # /api/currency/None/
        url = reverse('currency-detail', kwargs={'pk': old_currency.id})
        # <WSGIRequest: PUT '/api/currency/None/'>
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(currency_dict)
        )

        # return old obj in place of searching a obj in DB with pk=None
        mocker.patch.object(
            CurrencyViewSet,
            'get_object',
            return_value=old_currency
        )

        # patched so that we don't have to save updated obj
        # basically preventing executing of save() method
        mocker.patch.object(
            Currency,
            'save'
        )

        # get view for put:update request from model viewset
        view = CurrencyViewSet.as_view(
            {'put': 'update'}
        )

        response = view(request, pk=old_currency.id).render()
        assert response.status_code == 200
        # b'{"name":"Macedonian denar","code":"MKD","symbol":"$"}'
        assert json.loads(response.content) == currency_dict

    @pytest.mark.parametrize(
        'field',
        [
            ('name'),
            ('code'),
            ('symbol'),
        ]
    )
    def test_partical_update(self, mocker, rf, field):
        currency = CurrencyFactory.build()

        valid_field = currency.__dict__[field]
        # /api/currency/None/
        url = reverse(
            'currency-detail', kwargs={'pk': currency.id}
        )

        # <WSGIRequest: PATCH '/api/currency/None/'>
        request = rf.patch(
            url,
            content_type='application/json',
            data=json.dumps({field: valid_field})
        )

        mocker.patch.object(
            CurrencyViewSet, 'get_object', return_value=currency
        )
        mocker.patch.object(
            Currency, 'save'
        )

        view = CurrencyViewSet.as_view(
            {'patch': 'partial_update'}
        )

        response = view(request).render()

        assert response.status_code == 200
        # b'{"name":"Bermudian dollar","code":"BMD","symbol":"$"}'
        assert json.loads(response.content)[field] == valid_field

    def test_delete(self, mocker, rf):
        currency = CurrencyFactory.build()
        url = reverse('currency-detail', kwargs={'pk': currency.id})
        request = rf.delete(url)

        mocker.patch.object(
            CurrencyViewSet,
            'get_object',
            return_value=currency
        )
        
        del_mock = mocker.patch.object(
            Currency, 'delete'
        )

        view = CurrencyViewSet.as_view(
            {'delete': 'destroy'}
        )

        response = view(request).render()

        assert response.status_code == 204
        assert del_mock.assert_called


class TestTransactionViewSet:
    
    def test_list(self, mocker, rf):
        # /api/transaction/
        url = reverse('transaction-list')
        # <WSGIRequest: GET '/api/transaction/'>
        request = rf.get(url)

        qs = MockSet(
            FilledTransactionFactory.build(),
            FilledTransactionFactory.build(),
            FilledTransactionFactory.build()
        )

        mocker.patch.object(
            TransactionViewset,
            'get_queryset',
            return_value=qs
        )

        view = TransactionViewset.as_view(
            {'get': 'list'}
        )

        response = view(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_create(self, mocker, rf):
        # we create the Transaction instance without assigning Currency to it
        # in this way we do not need to save Currency object in DB. Remember 
        # Transaction object can only refer to Currency object if Currency instance 
        # have pk assigned to it which need saving it in DB.
 
        # {'email': 'hsmith@gmail.com', 'name': 'Melissa Baker'}
        valid_data_dict = factory.build(
            dict,
            FACTORY_CLASS=CurrencylessTransactionFactory
        )

        # provide currency CODE in place of currency obj
        # get a Currecny instance and let Transaction instance refer it
        currency = CurrencyFactory.build()

        # {'currency': 'BWP', 'email': 'hsmith@gmail.com', 'name': 'Melissa Baker'}
        valid_data_dict['currency'] = currency.code

        # /api/transaction/
        url = reverse('transaction-list')
        # <WSGIRequest: POST '/api/transaction/'>
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(valid_data_dict)
        )

        # this return the currency instance when serializer tries to get the 
        # saved instance of Currency withing DB using the Currency Code
        retrieve_currency = mocker.Mock(return_value=currency)
        SlugRelatedField.to_internal_value = retrieve_currency

        # prevent execution of save method in Transaction Model
        mocker.patch.object(
            Transaction, 'save'
        )

        view = TransactionViewset.as_view(
            {'post': 'create'}
        )
        response = view(request).render()

        assert response.status_code == 201
        assert json.loads(response.content) == valid_data_dict

    def test_retreive(self, mocker, rf):
        transaction = FilledTransactionFactory.build()
        # do not modified the actual __dict__ attribute of transaction
        # obj as that will determine the results
        expected_json = transaction.__dict__.copy()

        expected_json['link'] = transaction.link
        expected_json['uid'] = str(transaction.uid)
        expected_json['currency'] = transaction.currency.code
        expected_json.pop('_state')
        expected_json.pop('currency_id')
        # {'id': None, 'uid': '649b12b1-791d-4bd0-9dd3-6d0e4bb722f9', 'name': 'Charles Moran', 
        # 'email': 'vanessa38@yahoo.com', 'creation_date': None, 'payment_intent_id': 'abcdef', 
        # 'message': 'Time teacher prepare', 'link': 'http://127.0.0.1:8000/payment/None', 
        # 'currency': 'STD'}

        # /api/transaction/None/
        url = reverse('transaction-detail', kwargs={'pk': transaction.id})
        # <WSGIRequest: GET '/api/transaction/None/'>
        request = rf.get(url)

        TransactionViewset.get_queryset = mocker.Mock(
            return_value=MockSet(transaction)
        )

        # let related field of transaction retrieve the currency instance we created
        retrieve_currency = mocker.Mock(return_value=transaction.currency)
        StringRelatedField.to_internal_value = retrieve_currency

        view = TransactionViewset.as_view(
            {'get': 'retrieve'}
        )

        response = view(request, pk=transaction.id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_update(self, mocker, rf):
        # {'id': None, 'uid': '30f9b174-99b8-4f17-a204-a87b37d9fdda', 'name': 'Brianna Bowen', 
        # 'email': 'stacyhernandez@gmail.com', 'creation_date': None, 'payment_intent_id': 'abcdef', 
        # 'message': 'Kitchen second cover', 'link': 'http://127.0.0.1:8000/payment/None', 
        # 'currency': 'VEF'}
        old_transaction = FilledTransactionFactory.build()
        new_transaction = FilledTransactionFactory.build()
        # we like to update old_transaction's all fields with new_transaction
        transaction_json = TransactionInstanceToJson.convert(new_transaction)

        # we can't update currency as per our serializer
        # see this currency = serializers.StringRelatedField(read_only=True)
        transaction_json['currency'] = old_transaction.currency.code
        # and the UID field is uneditable so that too will remain same
        transaction_json['uid'] = str(old_transaction.uid)

        # /api/transaction/None/
        url = reverse('transaction-detail', kwargs={'pk': old_transaction.id})
        retrieve_currency = mocker.Mock(return_value=old_transaction.currency)
        SlugRelatedField.to_internal_value = retrieve_currency

        # get old instance on lookup
        mocker.patch.object(
            TransactionViewset,
            'get_object',
            return_value=old_transaction
        )

        # to prevent saving of updated instance, hence no DB call
        Transaction.save = mocker.Mock()

        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(transaction_json)
        )

        view = TransactionViewset.as_view(
            {'put': 'update'}
        )

        response = view(request, pk=old_transaction.id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == transaction_json

    @pytest.mark.parametrize(
        'field',
        [
            ('name'),
            ('message'),
            ('email'),
        ]
    )
    def test_partial_update(self, mocker, rf, field):
        old_transaction = FilledTransactionFactory.build()
        new_transaction = FilledTransactionFactory.build()
        valid_field_data = { field: new_transaction.__dict__[field]}
        # /api/transaction/None/
        url = reverse(
            'transaction-detail',
            kwargs={'pk': old_transaction.id}
        )

        SlugRelatedField.to_internal_value = mocker.Mock(
            return_value=old_transaction.currency
        )
        mocker.patch.object(
            TransactionViewset,
            'get_object',
            return_value=old_transaction
        )
        Transaction.save = mocker.Mock()

        request = rf.patch(
            url,
            content_type='application/json',
            data=json.dumps(valid_field_data)
        )

        view = TransactionViewset.as_view(
            {'patch': 'partial_update'}
        )

        response = view(request).render()

        assert response.status_code == 200
        assert json.loads(response.content)[field] == valid_field_data[field]

    def test_delete(self, mocker, rf):
        transaction = FilledTransactionFactory.build()
        # /api/transaction/None/
        url = reverse('transaction-detail', kwargs={'pk': transaction.id})
        
        mocker.patch.object(
            TransactionViewset, 
            'get_object', 
            return_value=transaction
        )
        del_mock = mocker.patch.object(
            Transaction, 'delete'
        )

        request = rf.delete(url)
        view = TransactionViewset.as_view(
            {'delete': 'destroy'}
        )

        response = view(request, pk=transaction.id).render()

        assert response.status_code == 204
        assert del_mock.assert_called
