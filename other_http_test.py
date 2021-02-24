# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=pointless-statement
'''Http tests for other.py'''
import time
import json
import urllib
import pytest
from other_functions import reset_all



BASE_URL = 'http://127.0.0.1:8001'

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
def register_user2():
    data = json.dumps({
        "email" : "z654321@unsw.edu.au",
        "password" : "password",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    return data

@pytest.fixture
def create_channel():
    data = json.dumps({               # create user
        "email" : "z1234567@unsw.edu.au",
        "password" : "abcd1234",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    token = payload["token"]
    data = json.dumps({              # create channel
        "token" : token,
        "name" : "new_channel",
        "is_public" : True
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/createe", data=data, \
        headers={'Content-Type': 'application/json'}, method='PUT')
    payload = json.load(urllib.request.urlopen(req))
    return (token, payload['channel_id'])

@pytest.fixture
def reset():
    reset_all()

def test_change_permission(register_user, register_user2, reset):
    reset
    data = register_user
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    token = payload['token']
    data = register_user2
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    u_id = payload["u_id"]
    data = json.dumps({
        "token" : token,
        "u_id" : u_id,
        "permission_id" : 1
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/admin/userpermission/change", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

def test_start_standup(reset, create_channel):
    reset
    token, channel_id = create_channel
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "length" : 10
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/standup/start", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {time.time() + 10}

def test_active_standup(reset, create_channel):
    reset
    token, channel_id = create_channel

    data = json.dumps({          # stand_up is not active
        "token" : token,
        "channel_id" : channel_id,
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/standup/active", data=data, \
        headers={'Content-Type': 'application/json'}, method='GET')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {False, None}

    data = json.dumps({           # active stand_up
        "token" : token,
        "channel_id" : channel_id,
        "length" : 10
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/standup/start", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    data = json.dumps({          # stand_up is active
        "token" : token,
        "channel_id" : channel_id,
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/standup/active", data=data, \
        headers={'Content-Type': 'application/json'}, method='GET')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {True, time.time() + 10}

def test_send_standup(reset, create_channel):
    reset
    token, channel_id = create_channel

    data = json.dumps({           # active stand_up
        "token" : token,
        "channel_id" : channel_id,
        "length" : 10
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/standup/start", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    data = json.dumps({           # stand_up is active
        "token" : token,
        "channel_id" : channel_id,
        "message" : 'I like banana'
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/standup/send", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

def test_reset_workspace(reset, create_channel):
    reset
    create_channel

    data = json.dumps({
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

def test_search_function(reset, create_channel):
    reset
    token, channel_id = create_channel

    data = json.dumps({           # send message
        "token" : token,
        "channel_id" : channel_id,
        "message" : 'I like banana'
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    data = json.dumps({           # search message
        "token" : token,
        "query_str" : 'I like banana'
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/search", data=data, \
        headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {"'I like banana'"}