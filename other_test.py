# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=pointless-statement
import time
import pytest
from user_functions import users_all
from error import InputError, AccessError
from auth_functions import auth_register, auth_login
from channels_functions import channels_create
from other_functions import search, reset_all, standup_start, \
    standup_active, standup_send, workspace_reset, user_permission

@pytest.fixture
def get_user():
    data = auth_register('jiahaozhang@unsw.edu.au', 'password', 'jiahao', 'zhang')
    token = data['token']
    channel_id = channels_create(token, 'New channel', True)
    return (token, channel_id,)

@pytest.fixture
def reset():
    reset_all()

def test_worksapce_reset(reset):
    reset
    data = auth_register('123456789@gmail.com', 'password', 'jiahao', 'zhang')
    token1 = data['token']
    assert workspace_reset() == {}
    with pytest.raises(AccessError):
        users_all(token1)
    ##assert channels_list(token) == {}

def test_set_user_permission(reset):
    reset
    data = auth_register('jiahaozhang@unsw.edu.au', 'password', 'jiahao', 'zhang')
    token = data['token']
    data = auth_register('123456789@gmail.com', 'password', 'jiahao', 'zhang')
    u_id1 = data['u_id']
    data1 = auth_register('jiahaozhang890@gmail.com', 'password', 'jiahao', 'zhang')
    u_id2 = data1['u_id']
    assert user_permission(token, u_id2, 1) == {}
    assert user_permission(token, u_id1, 1) == {}

def test_stand_up_start(reset, get_user):
    reset
    token, channel_id = get_user
    invaild_channel_id = -1
    assert standup_start(token, channel_id, 10) == {time.time() + 10}
    ## test for An active standup is currently running in this channel
    with pytest.raises(InputError):
        standup_start(token, channel_id, 10)
    with pytest.raises(InputError):## testt for invaild_channel_id
        standup_start(token, invaild_channel_id, 10)

def test_stand_up_active(reset, get_user):
    reset
    token, channel_id = get_user
    invaild_channel_id = -1
    assert standup_active(token, channel_id) == {False, None}
    standup_start(token, channel_id, 10)
    assert standup_active(token, channel_id) == {True, time.time() + 10}
    with pytest.raises(InputError):
        standup_start(token, invaild_channel_id, 10)

def test_stand_up_send(reset, get_user):
    reset
    token, channel_id = get_user
    invaild_channel_id = -1
    data1 = auth_register('jiahaozhang@unsw.edu.au', 'password', 'jiahao', 'zhang')
    token1 = data1['token']
    ## creat another user to test 'user is not a member of the channel'
    standup_start(token, channel_id, 10)
    assert standup_send(token, channel_id, 'I like banana') == {}

    time.sleep(10)
    with pytest.raises(InputError): ## test for No current active standup in channel
        standup_send(token, channel_id, 'I like banana')

    standup_start(token, channel_id, 10)
    with pytest.raises(InputError): ## test for invalid channel_id
        standup_send(token, invaild_channel_id, 'I like banana')

    with pytest.raises(InputError): ## test 'user is not a member of the channel'
        standup_send(token1, channel_id, 'I like banana')
    with pytest.raises(InputError): ## test for Message cannot be over 1000 characters long
        standup_send(token, channel_id, 'banan' * 205)



def get_token_via_name():
    data = auth_register('evert.chan@unsw.edu.au', 'password123', 'Evert', 'Chan')
    return data['token']

def get_token_via_email():
    data = auth_login('evert.chan@unsw.edu.au', 'password123')
    return data['token']

#Test if search function returns the same message as message inputed
def test_correct_query():
    query = 'Hello world'
    token = get_token_via_name()
    assert search(token, query)['messages'][0]['message'] == query

#Test if search returns nothing if given non-existing message
def test_incorrect_query():
    query = 'non-existing message'
    token = get_token_via_name()
    with pytest.raises(InputError):
        search(token, query)

def test_non_existing_string():
    query = 'non existing message'
    token = get_token_via_name()
    assert search(token, query)['messages'][0]['message'] != "query"