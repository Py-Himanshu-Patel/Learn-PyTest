import pytest
import json
import factory


from django.urls import reverse
from django_mock_queries.mocks import MockSet
from rest_framework.relations import RelatedField, SlugRelatedField


from apps.Payment.serializers import UnfilledTransactionSerializer, CurrencySerializer
from apps.Payment.views import CurrencyViewSet, TransactionViewset
from apps.Payment.models import Currency, Transaction
from tests.Payment.factory import CurrencyFactory, FilledTransactionFactory


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

