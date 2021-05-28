import pytest

def test_set_check_password1(create_user):
    print("Test 1")
    assert create_user.username == 'test'

def test_set_check_password2(create_user):
    print("Test 2")
    assert create_user.username == 'test'
