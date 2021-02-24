# pylint: disable=import-error
'''Channel tests for channel functions'''

import pytest
from channel_functions import channel_messages, channel_invite, channel_details
from channel_functions import channel_join, channel_leave, channel_addowner, channel_removeowner
from channels_functions import channels_create
from auth_functions import auth_register, reset_data
from message_functions import message_send
from error import InputError, AccessError

def test_channel_join():
    '''Function should allow authorised user to join channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    assert channel_join(token_two, channel_id['channel_id']) == {}

def test_channel_join_invalid_channel_id():
    '''Authorised user can't join channel with invalid channel id'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    assert channel_id['channel_id'] == 1
    with pytest.raises(InputError):
        channel_join(token_two, 2)

def test_channel_join_private_channel():
    '''Authorised user can't join private channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', False)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    with pytest.raises(AccessError):
        channel_join(token_two, channel_id['channel_id'])

def test_channel_leave():
    '''Authorised user is given permission to leave channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    channel_join(token_two, channel_id['channel_id'])
    assert channel_leave(token_two, channel_id['channel_id']) == {}

def test_channel_leave_invalid_channel_id():
    '''Authorised user can't use function with invalid channel_id'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    assert channel_id['channel_id'] == 1
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    channel_join(token_two, channel_id['channel_id'])
    with pytest.raises(InputError):
        channel_leave(token_two, 2)

def test_channel_leave_non_member():
    '''Authorised user can't use function if its not a channel member'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    with pytest.raises(AccessError):
        channel_leave(token_two, channel_id['channel_id'])

def test_channel_addowner():
    '''Function should add new user as owner of channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    other_user_id = data_two['u_id']
    assert channel_addowner(token, channel_id['channel_id'], other_user_id) == {}

def test_channel_addowner_twice():
    '''Function cannot add owner twice'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    other_user_id = data_two['u_id']
    channel_addowner(token, channel_id['channel_id'], other_user_id)
    with pytest.raises(InputError):
        channel_addowner(token, channel_id['channel_id'], other_user_id)

def test_channel_addowner_non_owner():
    '''Function cannot add owner to channel if authorised user is not owner'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    data_three = auth_register('z1234569@unsw.edu.au', 'cs1531', 'Yuri', 'Jo')
    other_user_id = data_three['u_id']
    with pytest.raises(AccessError):
        channel_addowner(token_two, channel_id['channel_id'], other_user_id)

def test_channel_removeowner():
    '''Function should remove owner based on their u_id in specified channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    other_user_id = data_two['u_id']
    channel_addowner(token, channel_id['channel_id'], other_user_id)
    assert channel_removeowner(token, channel_id['channel_id'], other_user_id) == {}

def test_removeowner_invalid_channel_id():
    '''Function won't run with invalid channel_id'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    assert channel_id['channel_id'] == 1
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    other_user_id = data_two['u_id']
    with pytest.raises(InputError):
        channel_removeowner(token, 2, other_user_id)

def test_removeowner_non_owner():
    '''Function cannot remove u_id from owners list if u_id is not channel owner'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    other_user_id = data_two['u_id']
    with pytest.raises(InputError):
        channel_removeowner(token, channel_id['channel_id'], other_user_id)

def test_removeowner_authorised_non_owner():
    '''Function won't run if authorised user is not owner of channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    user_two_id = data_two['u_id']
    channel_addowner(token, channel_id['channel_id'], user_two_id)
    data_three = auth_register('z1234569@unsw.edu.au', 'cs1531', 'Yuri', 'Jo')
    token_three = data_three['token']
    with pytest.raises(AccessError):
        channel_removeowner(token_three, channel_id['channel_id'], user_two_id)

def test_channel_details():
    '''Function should return some details of specified channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    user_id = data['u_id']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    user_two_id = data_two['u_id']
    channel_join(token_two, channel_id['channel_id'])
    channel_dict = channel_details(token, channel_id['channel_id'])
    assert channel_dict['name'] == 'Channel One'
    assert channel_dict['owner_members'] == [user_id]
    assert channel_dict['all_members'] == [user_id, user_two_id]

def test_details_invalid_channel_id():
    '''Function won't work if channel id is invalid'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channels_create(token, 'Channel One', True)
    with pytest.raises(InputError):
        channel_details(token, 2)

def test_details_invalid_channel_member():
    '''Function won't work if authorised user is not member of channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    with pytest.raises(AccessError):
        channel_details(token_two, channel_id['channel_id'])

def test_channel_messages():
    '''Shows one channel message after one was sent'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_id = message_send(token, channel_id['channel_id'], 'hi')
    message_dict = channel_messages(token, channel_id['channel_id'], 0)
    assert message_dict['start'] == 0
    assert message_dict['end'] == -1
    assert message_dict['messages'][0]['message_id'] == message_id['message_id']

def test_channel_messages_invalid_channel_id():
    '''Channel messages will not run with invalid channel ID'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_send(token, channel_id['channel_id'], 'hi')
    with pytest.raises(InputError):
        channel_messages(token, 2, 0)

def test_invalid_start_value():
    '''Channel messages will not work if start value is bigger than total messages'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_send(token, channel_id['channel_id'], 'hi')
    with pytest.raises(InputError):
        channel_messages(token, channel_id['channel_id'], 2)

def test_messages_nonmember():
    '''Channel messages will not work if there is non-channel member requesting'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    message_send(token, channel_id['channel_id'], 'Song Hayoung > Choi Yena')
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    with pytest.raises(AccessError):
        channel_messages(token_two, channel_id['channel_id'], 0)

def test_channel_invite():
    '''This channel will invite new user to channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    new_user_id = data_two['u_id']
    assert channel_invite(token, channel_id['channel_id'], new_user_id) == {}

def test_channel_invite_invalid_channel_id():
    '''New user can't be invited with invalid channel id'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    new_user_id = data_two['u_id']
    with pytest.raises(InputError):
        channel_invite(token, 2, new_user_id)

def test_channel_invite_invalid_user_id():
    '''New user can't be invited with invalid user id'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    new_user_id = data_two['u_id']
    with pytest.raises(InputError):
        channel_invite(token, 2, new_user_id-1)

def test_invite_nonmember():
    '''New user can't be invited if authorised user has not joined channel yet'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, 'Channel One', True)
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yena', 'Choi')
    token_two = data_two['token']
    data_three = auth_register('z1234569@unsw.edu.au', 'cs1531', 'Yuri', 'Jo')
    new_user_id = data_three['u_id']
    with pytest.raises(AccessError):
        channel_invite(token_two, channel_id['channel_id'], new_user_id)
