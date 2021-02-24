# pylint: disable=C0111
# pylint: disable=W0621
# pylint: disable=E0401
# pylint: disable=W0104

import pytest
from channels_functions import channels_list, channels_listall, channels_create
from channel_functions import channel_join, channel_leave
from auth_functions import auth_register, reset_data
from error import InputError

def test_channels_create():
    '''Function creates a new channel'''
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, "Channel One", True)
    assert channel_id['channel_id'] == 1

def test_channels_create_long_name():
    '''Cannot create channel if name is more than 20 characters'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    with pytest.raises(InputError):
        channels_create(token, "Yena's Army of Ducks Fan Club", True)

def test_channels_create_two_channels():
    '''Create two channels to compare their channel ids too'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, "Channel One", True)
    assert channel_id['channel_id'] == 1
    channel_two_id = channels_create(token, "Channel Two", False)
    assert channel_two_id['channel_id'] == 2

def test_channels_create_two_channels_same_name():
    '''Create two channels with same name and public value'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channel_id = channels_create(token, "UNSW Channel", True)
    assert channel_id['channel_id'] == 1
    channel_two_id = channels_create(token, "UNSW Channel", True)
    assert channel_two_id['channel_id'] == 2

def test_channels_create_empty_is_public_value():
    '''If the is_public value is empty, it creates the private channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    assert bool('') is False
    channel_id = channels_create(token, "Channel One", '')
    assert channel_id['channel_id'] == 1

def test_channels_list_one_channel():
    '''Returns a list of 1 channel that the authorised user is part of'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']

    #Creates Channel One under User One's token which adds user to channel
    channels_create(token, "Channel One", True)
    user_one_channel_list = channels_list(token)
    assert len(user_one_channel_list['channels']) == 1

def test_channels_list_two_channels():
    '''Returns a list of 2 channels that the authorised user is part of'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']

    #Creates Channel One under User One's token which adds user to channel
    channels_create(token, "Channel One", True)
    channel_list = channels_list(token)
    assert len(channel_list['channels']) == 1

    #Creates Channel Two under User One's token which adds user to channel
    channels_create(token, "Channel Two", True)
    user_one_channel_list = channels_list(token)
    assert len(user_one_channel_list['channels']) == 2

def test_channels_list_two_channels_create_three_channels():
    '''Creates 3 channels but authorised user is part of 2 of them'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']

    #Creates Channel One under User One's token which adds user to channel
    channels_create(token, "Channel One", True)
    user_one_channel_list = channels_list(token)
    assert len(user_one_channel_list['channels']) == 1

    #Creates Channel Two under User One's token which adds user to channel
    channels_create(token, "Channel Two", True)
    user_one_channel_list = channels_list(token)
    assert len(user_one_channel_list['channels']) == 2

    #Register User Two
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yuri', 'Jo')
    token_two = data_two['token']

    #Creates Channel Three under User Two's token which adds user to channel
    channels_create(token_two, "Channel Three", True)

    # Asserts that User One is not part of Channel Three by checking User
    # One's channels list under their token
    user_one_channel_list = channels_list(token)
    assert len(user_one_channel_list['channels']) == 2

    #Checks User Two's channels list
    user_two_channel_list = channels_list(token_two)
    assert len(user_two_channel_list['channels']) == 1

def test_channels_list_zero_channels():
    '''Creates 0 channels and checks if user is part of no channels'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    user_one_channel_list = channels_list(token)
    assert bool(user_one_channel_list['channels']) is False

def test_channels_list_under_channel_join():
    '''User 1 make 2 channels, User 2 joins them and channel list updates'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']

    #Creates Channel One under User One's token which adds user to channel
    channel_id = channels_create(token, "Channel One", True)
    user_one_channel_list = channels_list(token)
    assert len(user_one_channel_list['channels']) == 1

    #Creates Channel Two under User One's token which adds user to channel
    channel_two_id = channels_create(token, "Channel Two", True)
    user_one_channel_list = channels_list(token)
    assert len(user_one_channel_list['channels']) == 2

    #Register User Two
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yuri', 'Jo')
    token_two = data_two['token']

    #Assert that User Two's channel_list is empty
    user_two_channel_list = channels_list(token_two)
    assert bool(user_two_channel_list['channels']) is False

    #User Two joins Channel One and channel list is updated
    channel_join(token_two, channel_id['channel_id'])
    user_two_channel_list = channels_list(token_two)
    assert len(user_two_channel_list['channels']) == 1

    #User Two joins Channel Two and channel list is updated
    channel_join(token_two, channel_two_id['channel_id'])
    user_two_channel_list = channels_list(token_two)
    assert len(user_two_channel_list['channels']) == 2

def test_channels_list_under_channel_join_and_leave():
    '''Tests if channel_leave will impact on channels_list'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']

    #Creates Channel One under User One's token which adds user to channel
    channel_id = channels_create(token, "Channel One", True)
    user_one_channel_list = channels_list(token)
    assert len(user_one_channel_list['channels']) == 1

    #Creates Channel Two under User One's token which adds user to channel
    channel_two_id = channels_create(token, "Channel Two", True)
    user_one_channel_list = channels_list(token)
    assert len(user_one_channel_list['channels']) == 2

    #Register User Two
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yuri', 'Jo')
    token_two = data_two['token']

    #Assert that User Two's channel_list is empty
    user_two_channel_list = channels_list(token_two)
    assert bool(user_two_channel_list['channels']) is False

    #User Two joins Channel One and channel list is updated
    channel_join(token_two, channel_id['channel_id'])
    user_two_channel_list = channels_list(token_two)
    assert len(user_two_channel_list['channels']) == 1

    #User Two joins Channel Two and channel list is updated
    channel_join(token_two, channel_two_id['channel_id'])
    user_two_channel_list = channels_list(token_two)
    assert len(user_two_channel_list['channels']) == 2

    #User Two leaves Channel One and channel_list is updated
    channel_leave(token_two, channel_two_id['channel_id'])
    user_two_channel_list = channels_list(token_two)
    assert len(user_two_channel_list['channels']) == 1

def test_channels_listall():
    '''Creates 1 channel under User One's token and list 1 channel'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']

    #Creates Channel One under User One's token which adds user to channel
    channels_create(token, "Channel One", True)
    channels_list = channels_listall(token)
    assert len(channels_list['channels']) == 1

def test_channels_listall_two_users():
    '''User One makes 1 channel, User One and Two checks channel list'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']

    #Creates Channel One under User One's token which adds user to channel
    channels_create(token, "Channel One", True)
    channels_list = channels_listall(token)
    assert len(channels_list['channels']) == 1

    #User Two is registered and accesses channel list
    data_two = auth_register('z1234568@unsw.edu.au', 'cs1531', 'Yuri', 'Jo')
    token_two = data_two['token']
    channels_list = channels_listall(token_two)
    assert len(channels_list['channels']) == 1

def test_channels_listall_zero_channels():
    '''User One checks empty list of channels'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']
    channels_list = channels_listall(token)
    assert bool(channels_list['channels']) is False

def test_channels_listall_two_channels():
    '''Creates 2 channels under User One's token and list 2 channels'''
    reset_data()
    data = auth_register('z1234567@unsw.edu.au', 'cs1531', 'Kevin', 'Trang')
    token = data['token']

    #Creates Channel One under User One's token which adds user to channel
    channels_create(token, "Channel One", True)
    channels_list = channels_listall(token)
    assert len(channels_list['channels']) == 1

    #Creates Channel Two under User One's token which adds user to channel
    channels_create(token, "Channel Two", True)
    channels_list = channels_listall(token)
    assert len(channels_list['channels']) == 2
