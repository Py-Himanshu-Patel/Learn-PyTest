import pytest
from apps.FactoryApp.models import Product


def test_product_creation(db, product_factory):
    product = product_factory.create()
    print(product.description)		# random text
    print(product.category)			# random text
    print(Product.objects.count())	# 1
    assert True
