import pytest

@pytest.fixture()
def fixture_1():
    print('Fixture 1')
    return 1

def test_example1(fixture_1):
    print('Example 1')
    assert 1 == fixture_1

def test_example2(fixture_1):
    print('Example 2')
    assert 1 == fixture_1
