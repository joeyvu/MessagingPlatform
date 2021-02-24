'''Http tests for channel.py'''

import json
import urllib
import flask
import pytest
from error import InputError, AccessError
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

@pytest.fixture
def test_channel_invite(register_user, reset):
    '''Tests if the authorised user can invite new user to channel'''
    reset
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "user_id" : u_id
     }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", data=data, \
        headers={'Content-Type': 'application/json'}, method='POST')
    payload = json.load(urllib.request.urlopen(req))
    assert payload = {}

@pytest.fixture
def test_channel_details(register_user, reset):
    '''Tests if the authorised user can receive channel details'''
    reset
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
     }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/details", data=data, \
        headers={'Content-Type': 'application/json'}, method='GET')
    payload = json.load(urllib.request.urlopen(req))
    assert payload = {name, owner_members, all_members}

@pytest.fixture
def test_channel_messages(register_user, reset):
    '''Tests if the functions up to 50 messages based on starting value'''
    reset
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "start" : start
     }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/messages", data=data, \
        headers={'Content-Type': 'application/json'}, method='GET')
    payload = json.load(urllib.request.urlopen(req))
    assert payload = {messages, start, end}
    
    @pytest.fixture
    def test_channel_join(register_user, reset):
    '''Tests removing an owner of a channel'''
    reset
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "user_id" : u_id
     }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/addowner", data=data, \
        headers={'Content-Type': 'application/json'}, method='POST')
    payload = json.load(urllib.request.urlopen(req))
    assert payload = {}
    
    @pytest.fixture
    def test_channel_remove(register_user, reset):
    '''Tests if a user can be removed from a channel'''
    reset
    token = register_user['token']
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "user_id" : u_id
     }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data=data, \
        headers={'Content-Type': 'application/json'}, method='POST')
    payload = json.load(urllib.request.urlopen(req))
    assert payload = {}
