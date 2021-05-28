import pytest

from pytest_factoryboy import register
from .factory import UserFactory

register(UserFactory)	# now fixture to access this factory is user_factory
