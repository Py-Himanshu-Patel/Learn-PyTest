import pytest

@pytest.mark.skip
def test_example2():
	print("Inside string test")
	assert 'Hi' == 'Hi'

@pytest.mark.xfail
def test_example1():
	assert 1 == 1

@pytest.mark.xfail
def test_example3():
	assert 1 == 2
