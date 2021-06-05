import pytest

@pytest.fixture
def yield_fixture():
	print("Start Test Phase")
	yield 1
	print("End Test Phase")

def test_example(yield_fixture):
	print('Example Test Case')
	assert 1 == yield_fixture
