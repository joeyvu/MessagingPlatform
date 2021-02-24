# pylint: disable=E0401
# pylint: disable=C0111
# pylint: disable=W0621
# pylint: disable=W0104
# pylint: disable=W0105


import json
import urllib.request
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


''' test user viewing channel'''
def test_list_channel(register_user, reset):
    reset
    token, u_id = register_user
    data = json.dumps({
        "token" : token,
        "u_id" : u_id
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/listall", data=data, \
        headers={'Content-Type': 'application/json'}, method='GET')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {dict}


''' tests user viewing all channels'''
def test_channels_all(register_user, reset):
    reset
    token = register_user["token"]
    data = json.dumps({
        "token" : token
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/listall", data=data, \
        headers={'Content-Type': 'application/json'}, method='GET')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {list}


''' tests user creating a channel'''
def test_create_channels(register_user):
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "name" : "new_channel",
        "is_public" : True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {int}
