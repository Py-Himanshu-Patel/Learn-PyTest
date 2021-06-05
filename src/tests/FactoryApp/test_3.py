import pytest
from apps.FactoryApp.models import Product

def test_product_creation(db, product_factory):
	product = product_factory.create()
	print(product.description)
	print(product.category)
	print(Product.objects.count())
	assert True
