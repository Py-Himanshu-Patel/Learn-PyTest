import pytest

def test_create_user_factory(create_new_user):
	print(create_new_user.first_name)
	assert  create_new_user.first_name == "user_firstname"
