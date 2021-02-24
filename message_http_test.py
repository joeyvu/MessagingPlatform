# pylint: disable=redefined-outer-name
# pylint: disable=unidiomatic-typecheck
# pylint: disable=pointless-statement
# pylint: disable=unused-variable
# pylint: disable=unused-argument


'''Http tests for message.py'''

import json
import urllib
import pytest
from auth_functions import reset_data

BASE_URL = 'http://127.0.0.1:8080'

@pytest.fixture
def register_user():
    '''Registers a user'''
    data = json.dumps({
        "email" : "z1234567@unsw.edu.au",
        "password" : "abcd1234",
        "name_first" : "John",
        "name_last" : "Smith"
    }).encode('utf-8')
    return data

@pytest.fixture
def login_user():
    '''User will login'''
    data = json.dumps({
        "email" : "z1234567@unsw.edu.au",
        "password" : "abcd1234",
    }).encode('utf-8')
    return data

@pytest.fixture
def reset():
    '''Resets the data'''
    reset_data()

def test_message_remove(register_user, reset):
    '''Tests if a message can be removed'''
    reset
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "message_id" : 1
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/remove", data=data, \
        headers={'Content-Type': 'application/json'}, method='DELETE')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

def test_message_edit(register_user, reset):
    '''Tests if the message can be edited'''
    reset
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "message_id" : 1,
        "message" : 'abc'
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/edit", data=data, \
       headers={'Content-Type': 'application/json'}, method='PUT')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

def test_message_react(register_user, reset):
    '''Tests if the message can be reacted'''
    reset
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "message_id" : 1,
        "react_id" : 1
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/react", data=data, \
        headers={'Content-Type': 'application/json'}, method='POST')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}

def test_message_unreact(register_user, reset):
    '''Tests if the message can be unreacted'''
    reset
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "message_id" : 1,
        "react_id" : 1
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/unreact", data=data, \
        headers={'Content-Type': 'application/json'}, method='POST')
    payload = json.load(urllib.request.urlopen(req))
    assert payload == {}
