# fixtures or factory declared here will be accessible to all the tests of all apps

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient
