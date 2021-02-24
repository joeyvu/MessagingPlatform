# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=pointless-statement
# pylint: disable=import-error

'''Includes tests for auth_functions.py.'''
import pytest
from auth_functions import auth_login, auth_logout, auth_register, reset_data
from error import InputError

@pytest.fixture
def get_new_user():
    data = auth_register('z1234567@unsw.edu.au', 'a1b2c3d4e5', 'John', 'Smith')
    return (data['u_id'], data['token'])

@pytest.fixture
def reset():
    reset_data()

def test_register(get_new_user):
    u_id, token = get_new_user
    assert isinstance(u_id, int)
    assert isinstance(token, str)

def test_register_short_password(reset):
    reset
    with pytest.raises(InputError):
        auth_register('z1234567@unsw.edu.au', 'abcd', 'John', 'Smith')

def test_register_invalid_email(reset):
    reset
    with pytest.raises(InputError):
        auth_register('z1234567.unsw', 'a1b2c3d4e5', 'John', 'Smith')

def test_register_invalid_first(reset):
    reset
    with pytest.raises(InputError):
        auth_register('z1234567@unsw.edu.au', 'a1b2c3d4e5', 'John' * 13, 'Smith')
        auth_register('z1234567@unsw.edu.au', 'a1b2c3d4e5', '', 'Smith')

def test_register_invalid_last(reset):
    reset
    with pytest.raises(InputError):
        auth_register('z1234567@unsw.edu.au', 'a1b2c3d4e5', 'John', 'Smith' * 11)
        auth_register('z1234567@unsw.edu.au', 'a1b2c3d4e5', 'John', '')

def test_register_twice(get_new_user, reset):
    reset
    get_new_user
    with pytest.raises(InputError):
        auth_register('z1234567@unsw.edu.au', 'a1b2c3d4e5', 'John', 'Smith')

def test_login(get_new_user, reset):
    reset
    u_id1, token1 = get_new_user
    results2 = auth_login('z1234567@unsw.edu.au', 'a1b2c3d4e5')
    u_id2 = results2['u_id']
    token2 = results2['token']

    assert u_id1 == u_id2
    assert token1 == token2

def test_login_invalid_email(reset):
    reset
    with pytest.raises(InputError):
        auth_login('z1234567.unsw', 'a1b2c3d4e5')

def test_login_email_not_registered(reset):
    reset
    with pytest.raises(InputError):
        auth_login('z7654321@unsw.edu.au', 'random123')

def test_login_incorrect_password(get_new_user, reset):
    reset
    get_new_user
    with pytest.raises(InputError):
        auth_login('z1234567@unsw.edu.au', 'wrongpassword')

def test_login_no_input(reset):
    reset
    with pytest.raises(InputError):
        auth_login('', '')

def test_logout(get_new_user, reset):
    reset
    token = get_new_user["token"]
    assert auth_logout(token) == {'is_success' : True}
