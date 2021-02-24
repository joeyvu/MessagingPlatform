'''Http tests for user.py'''
# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=pointless-statement
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
def reset():
    reset_data()

def test_setname(register_user, reset):
    reset
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    token = payload["token"]
    u_id = payload["u_id"]
    data = json.dumps({
        "token" : token,
        "name_first" : "Jim",
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setname", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

    ##use user_profile to check if the name is change
    querystring = urllib.parse.urlencode({
        'token' : token,
        'u_id' : u_id
    })
    req = (f"{BASE_URL}/user/profile?{querystring}")
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {
        'u_id': u_id,
        "email" : "z1234567@unsw.edu.au",
        "name_first" : "Jim",
        "name_last" : "Smith",
        'handle_str': 'johnsmith'
    }

    ##error case test
    data = json.dumps({
        "token" : token,
        "name_first" : "i" * 60,
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setname", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))

    data = json.dumps({
        "token" : token,
        "name_first" : "",
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setname", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))


def test_setemail(register_user, reset):
    reset
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    token = payload["token"]
    u_id = payload["u_id"]
    data = json.dumps({
        "token" : token,
        "email" : "z7654321@unsw.edu.au"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setemail", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

    ## check login with new eamil
    data = json.dumps({
        "email" : "z7654321@unsw.edu.au",
        "password" : "abcd1234",
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    ##use user_profile to check if the email is change
    querystring = urllib.parse.urlencode({
        'token' : payload['token'],
        'u_id' : payload['u_id']
    })
    req = (f"{BASE_URL}/user/profile?{querystring}")
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {
        'u_id': u_id,
        "email" : "z7654321@unsw.edu.au",
        "name_first" : "John",
        "name_last" : "Smith",
        'handle_str': 'johnsmith'
    }
    ## error case for eamil is already used
    ## get another user
    data = json.dumps({
        "email" : "z156435@unsw.edu.au",
        "password" : "abcd1234",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    ## set new user's eamil an used eamil
    data = json.dumps({
        "token" : payload['token'],
        "email" : "z7654321@unsw.edu.au"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setemail", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))



def test_sethandle(register_user, reset):
    reset
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    token = payload["token"]
    data = json.dumps({
        "token" : token,
        "handle_str" : "jsmith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/sethandle", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

    ##error case test
    data = json.dumps({
        "token" : token,
        "handle_str" : "i" * 40
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/sethandle", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))

    ## error case for handle_str is already used
    ## get another user
    data = json.dumps({
        "email" : "z156435@unsw.edu.au",
        "password" : "abcd1234",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    ## set new user's handle_str an used eamil
    data = json.dumps({
        "token" : payload['token'],
        "handle_str" : 'jsmith'
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/sethandle", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    with pytest.raises(urllib.error.HTTPError):
        payload = json.load(urllib.request.urlopen(req))


def test_profile(register_user, reset):
    reset
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    token = payload["token"]
    u_id = payload["u_id"]
    querystring = urllib.parse.urlencode({
        'token' : token,
        'u_id' : u_id
    })
    req = (f"{BASE_URL}/user/profile?{querystring}")
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {
        'u_id': u_id,
        "email" : "z1234567@unsw.edu.au",
        "name_first" : "John",
        "name_last" : "Smith",
        'handle_str': 'johnsmith'
    }
    ## test for check another user's profile
    ## get another user
    data = json.dumps({
        "email" : "z156435@unsw.edu.au",
        "password" : "abcd1234",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    ## check another user
    querystring = urllib.parse.urlencode({
        'token' : token,
        'u_id' : payload['u_id']
    })
    req = (f"{BASE_URL}/user/profile?{querystring}")
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {
        'u_id': payload['u_id'],
        "email" : "z156435@unsw.edu.au",
        "name_first" : "John",
        "name_last" : "Smith",
        'handle_str': 'johnsmith'
    }


def test_users_all(register_user, reset):
    reset
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    token = payload["token"]
    u_id = payload["u_id"]
    querystring = urllib.parse.urlencode({
        "token" : token,
    })
    req = (f"{BASE_URL}/users/all?{querystring}")
    payload = json.load(urllib.request.urlopen(req))
    assert payload == [{
        'u_id': u_id,
        'email': 'z1234567@unsw.edu.au',
        'name_first': 'John',
        'name_last': 'Smith',
        'handle_str': 'johnsmith',
    }]
    ##test 2 user
    ## get another user
    data = json.dumps({
        "email" : "z156435@unsw.edu.au",
        "password" : "abcd1234",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    u_id1 = payload['u_id']
    ## user_all
    querystring = urllib.parse.urlencode({
        "token" : token,
    })
    req = (f"{BASE_URL}/users/all?{querystring}")
    payload = json.load(urllib.request.urlopen(req))
    assert payload == [{
        'u_id': u_id,
        'email': 'z1234567@unsw.edu.au',
        'name_first': 'John',
        'name_last': 'Smith',
        'handle_str': 'johnsmith',
    }, {
        'u_id': u_id1,
        "email" : "z156435@unsw.edu.au",
        "name_first" : "John",
        "name_last" : "Smith",
        'handle_str': 'johnsmith'
    }]

