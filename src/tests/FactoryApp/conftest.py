import pytest

from pytest_factoryboy import register
from .factory import UserFactory, ProductFactory, CategoryFactory

# now fixture will access this factory as user_factory
register(UserFactory)	
register(ProductFactory)
register(CategoryFactory)

# use a fixture to access database while using 
# factory and prepare data for test
@pytest.fixture
def create_user(db, user_factory):
	user = user_factory.create()
	return user
