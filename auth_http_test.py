# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=unidiomatic-typecheck
# pylint: disable=pointless-statement
# pylint: disable=unused-variable
# pylint: disable=unused-argument

'''Http tests for auth.py.'''
import json
import urllib
import pytest
from auth_functions import reset_data

BASE_URL = 'http://127.0.0.1:8080'

@pytest.fixture
def register_user():
    data = json.dumps({
        "email" : "z1234567@unsw.edu.au",
        "password" : "abcd1234",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    return data

@pytest.fixture
def login_user():
    data = json.dumps({
        "email" : "z1234567@unsw.edu.au",
        "password" : "abcd1234",
    }).encode('utf-8')
    return data

@pytest.fixture
def reset():
    reset_data()

def test_auth_register(register_user, reset):
    '''Http test for /auth/register.'''
    reset
    # Registers a user, ensures that
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    assert type(payload["u_id"]) == int
    assert type(payload["token"]) == str

def test_auth_logout(register_user, reset):
    '''Tests if a user successfully registers and logs out.'''
    reset
    # Register a user
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    # Register again with the same email
    data = json.dumps({
        "token" : str(payload["token"])
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

def test_auth_login(register_user, login_user, reset):
    '''Tests if a user has successfully logged in.'''
    reset
    # Register a user
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    # Log user out to log back in
    data = json.dumps({
        "token" : str(payload["token"])
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    # Log user back in
    data = login_user
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

def test_multiple_users(register_user, login_user, reset):
    '''Tests auth functions with multiple users in its database.'''
    # Register user 1
    data1 = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data1, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    token1 = str(payload["token"])

    # Register user 2
    data2 = json.dumps({
        "email" : "z7654321@unsw.edu.au",
        "password" : "1234abcd",
        "name_first" : "Billy",
        "name_last" : "Jones"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data2, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    token2 = str(payload["token"])

    # Logout user 1
    data = json.dumps({
        "token" : token1
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    # Logout user 2
    data = json.dumps({
        "token" : token2
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    # Log user1 back in
    data = login_user
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    # Log user2 back in
    data = json.dumps({
        "email" : "z7654321@unsw.edu.au",
        "password" : "1234abcd",
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

def test_register_email_error(reset):
    '''Tests if an error is raised when invalid email is input.'''
    reset
    data = json.dumps({
        "email" : "z1234567",
        "password" : "abcd1234",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))

def test_register_password_error(reset):
    '''Tests if an error is raised when invalid password is input.'''
    reset
    data = json.dumps({
        "email" : "z1234567@unsw.edu.au",
        "password" : "a",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))

def test_register_name_first_error(reset):
    '''Tests if an error is raised when invalid first name is input.'''
    reset
    data = json.dumps({
        "email" : "z1234567@unsw.edu.au",
        "password" : "abcd1234",
        "name_first" : "John"*15,
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))

def test_register_name_last_error(reset):
    '''Tests if an error is raised when invalid last name is input.'''
    reset
    data = json.dumps({
        "email" : "z1234567@unsw.edu.au",
        "password" : "abcd1234",
        "name_first" : "John",
        "name_last" : "Smith"*12
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))

def test_login_error(register_user, reset):
    '''Tests if an error is raised when wrong password is input at login.'''
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    data = json.dumps({
        "email" : "z1234567@unsw.edu.au",
        "password" : "wrongpassword"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=data, \
        headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))
