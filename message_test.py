'''Message tests for message_functions'''

import pytest
from auth_functions import auth_register
from message_functions import message_send, message_remove, message_edit
from message_functions import message_react, message_unreact, message_pin, message_unpin
from error import InputError, AccessError
from channels_functions import channels_create, reset_data
from channel_functions import channel_join

def test_message_send():
    '''Send a normal message such as 'Hello World'''
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    assert isinstance(message_id['message_id'], int) is True

def test_message_send_long_string():
    '''Can't send message with more than 1000 characters'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    with pytest.raises(InputError):
        message_send(token, channel_id['channel_id'], 'he' * 1000)

def test_message_send_in_wrong_channel():
    '''Send message in a channel that the user has not joined'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    assert channel_id['channel_id'] == 1
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token_two = data_two['token']
    with pytest.raises(AccessError):
        message_send(token_two, channel_id['channel_id'], 'hello')

def test_message_send_link():
    '''A URL link will be sent as a string instead of an actual link'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message = 'https://www.google.com/'
    assert isinstance(message, str) is True
    message_id = message_send(token, channel_id['channel_id'], 'https://www.google.com/')
    assert isinstance(message_id['message_id'], int) is True

def test_message_remove():
    '''This function will remove a message'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    assert message_remove(token, message_id['message_id']) == {}

def test_remove_twice():
    '''Cannot remove a message twice'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    message_remove(token, message_id['message_id'])
    with pytest.raises(InputError):
        message_remove(token, message_id['message_id'])

def test_remove_other():
    '''Cannot remove another user's message when user is not owner'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    data_two = auth_register('z1234568@unsw.edu.au', 'IZ*ONE', 'Yena', 'Choi')
    token_two = data_two['token']
    channel_join(token_two, channel_id['channel_id'])
    with pytest.raises(AccessError):
        message_remove(token_two, message_id['message_id'])

def test_message_edit():
    '''This function will edit the message into a non-empty string'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'UNSW < USYD')
    message_edit(token, message_id['message_id'], 'UNSW > USYD')
    assert message_edit(token, message_id['message_id'], 'UNSW > USYD') == {}

def test_edit_other():
    '''Cannot edit another user's message when not admin/owner'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    data_two = auth_register('z1234568@unsw.edu.au', 'IZ*ONE', 'Yena', 'Choi')
    token_two = data_two['token']
    channel_join(token_two, channel_id['channel_id'])
    with pytest.raises(AccessError):
        message_edit(token_two, message_id['message_id'], 'Promote IZ*ONE')

def test_message_edit_empty():
    '''If the message is edited into an empty string, it'll be deleted'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'UNSW < USYD')
    assert message_edit(token, message_id['message_id'], '') == {}

def test_message_pin():
    '''Message will be pinned on the chat'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    assert message_pin(token, message_id['message_id']) == {}

def test_message_invalid_pin():
    '''Pinned message will not be pinned again'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    message_pin(token, message_id['message_id'])
    with pytest.raises(InputError):
        message_pin(token, message_id['message_id'])

def test_message_unpin():
    '''Message will be unpinned on the chat'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    message_pin(token, message_id['message_id'])
    assert message_unpin(token, message_id['message_id']) == {}

def test_message_invalid_unpin():
    '''Unpinned message will not be unpinned again'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    message_pin(token, message_id['message_id'])
    message_unpin(token, message_id['message_id'])
    with pytest.raises(InputError):
        message_unpin(token, message_id['message_id'])

def test_message_react():
    '''Message will be reacted on the chat'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    assert message_react(token, message_id['message_id'], 1) == {}

def test_message_invalid_react():
    '''Reacted message will not be reacted again'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    message_react(token, message_id['message_id'], 1)
    with pytest.raises(InputError):
        message_react(token, message_id['message_id'], 1)

def test_message_invalid_react_id_in_react():
    '''Message will be not reacted with invalid react id on the chat'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    with pytest.raises(InputError):
        message_react(token, message_id['message_id'], 2)

def test_message_unreact():
    '''Message will be unreacted on the chat'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    message_react(token, message_id['message_id'], 1)
    assert message_unreact(token, message_id['message_id'], 1) == {}

def test_message_invalid_unreact():
    '''Unreacted message will not be unreacted again'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    message_react(token, message_id['message_id'], 1)
    message_unreact(token, message_id['message_id'], 1)
    with pytest.raises(InputError):
        message_unreact(token, message_id['message_id'], 1)

def test_message_invalid_react_id_in_unreact():
    '''Message will not be unreacted with invalid react id on the chat'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'Hello World')
    message_react(token, message_id['message_id'], 1)
    with pytest.raises(InputError):
        message_unreact(token, message_id['message_id'], 2)
