import json

import pytest
from apps.Payment.models import Currency, Transaction
from apps.Payment.serializers import (CurrencySerializer,
                                      UnfilledTransactionSerializer)
from apps.Payment.views import CurrencyViewSet, TransactionViewset
from django.urls import reverse
from django_mock_queries.mocks import MockSet
from rest_framework.relations import SlugRelatedField
from tests.Payment.factory import (CurrencyFactory,
                                   CurrencylessTransactionFactory,
                                   FilledTransactionFactory,
                                   TransactionFactory)

import factory


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

    def test_retrive(self, mocker, rf):
        pass
