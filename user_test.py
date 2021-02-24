# pylint: disable=missing-docstring
import pytest
from user_functions import user_profile, reset_all, user_profile_setname, \
    user_profile_setemail, user_profile_sethandle, users_all
from auth_functions import auth_register, auth_login
from error import InputError


def test_user_profile():
    #register an user for test purpose
    reset_all()
    data = auth_register('123456789@gmail.com', 'password', 'jiahao', 'zhang')
    u_id1 = data['u_id']
    token1 = data['token']
    data1 = auth_register('jiahaozhang890@gmail.com', 'password', 'jiahao', 'zhang')
    u_id2 = data1['u_id']
    #sample invalid id and token
    invalid_u_id = -1

    assert user_profile(token1, u_id1) == {
        'u_id': u_id1,
        'email': '123456789@gmail.com',
        'name_first': 'jiahao',
        'name_last': 'zhang',
        'handle_str': 'jiahaozhang',
    }
    ## test to check another user
    assert user_profile(token1, u_id2) == {
        'u_id': u_id2,
        'email': 'jiahaozhang890@gmail.com',
        'name_first': 'jiahao',
        'name_last': 'zhang',
        'handle_str': 'jiahaozhang',
    }
    with pytest.raises(InputError):
        user_profile(token1, invalid_u_id)

def test_user_profile_setname():
    reset_all()
    data = auth_register('123456789@gmail.com', 'password', 'jiahao', 'zhang')
    u_id1 = data['u_id']
    token1 = data['token']
    assert user_profile_setname(token1, 'alen', 'banana') == {}

	#show user profile after successful change
    assert user_profile(token1, u_id1) == {
        'u_id': u_id1,
        'email': '123456789@gmail.com',
        'name_first': 'alen',
        'name_last': 'banana',
        'handle_str': 'jiahaozhang',
    }
    #test for wrong input
    with pytest.raises(InputError):
        user_profile_setname(token1, 'i' * 60, 'banana')

    with pytest.raises(InputError):
        user_profile_setname(token1, 'alen', 'i' * 60)

    with pytest.raises(InputError):
        user_profile_setname(token1, 'alen', '')
    with pytest.raises(InputError):
        user_profile_setname(token1, '', 'banana')


def test_user_profile_setemail():
    reset_all()
    data1 = auth_register('jiahaozhang890@gmail.com', 'password', 'jiahao', 'zhang')
    u_id1 = data1['u_id']
    token1 = data1['token']
    data2 = auth_register('alenbanana@gmail.com', 'password', 'jiahao', 'zhang')
    token2 = data2['token']
    assert user_profile_setemail(token1, 'jiahaozhang@gmail.com') == {}
    #token changed after successful change email
    #check for new eamil login
    data3 = auth_login('jiahaozhang@gmail.com', 'password')
    token3 = data3['token']
    assert user_profile(token3, u_id1) == {
        'u_id': u_id1,
        'email': 'jiahaozhang@gmail.com',
        'name_first': 'jiahao',
        'name_last': 'zhang',
        'handle_str': 'jiahaozhang',
    }


    ##token1 = auth_login('jiahaozhang@gmail.com','password')['token']

    with pytest.raises(InputError):
        user_profile_setemail(token3, '5')
    with pytest.raises(InputError):
        user_profile_setemail(token3, 'alenbanana@gmail.com')
    with pytest.raises(InputError):
        user_profile_setemail(token2, 'jiahaozhang@gmail.com')

def test_user_profile_sethandle():
    reset_all()
    data1 = auth_register('jiahaozhang890@gmail.com', 'password', 'jiahao', 'zhang')
    u_id1 = data1['u_id']
    token1 = data1['token']
    data2 = auth_register('alenbanana890@gmail.com', 'password', 'jiahao', 'zhang')
    token2 = data2['token']
    assert user_profile_sethandle(token1, 'jiah') == {}
    assert user_profile(token1, u_id1) == {
        'u_id': u_id1,
        'email': 'jiahaozhang890@gmail.com',
        'name_first': 'jiahao',
        'name_last': 'zhang',
        'handle_str': 'jiah',
    }
    assert user_profile_sethandle(token2, 'alen') == {}
    #token changed after successful change handle_str
    #token1 = auth_login('jiahaozhang890@gmail.com','123456')['token']
    #token2 = auth_login('alenbanana@gmail.com','123456')['token']

    with pytest.raises(InputError):
        user_profile_sethandle(token2, 'jiah')

    with pytest.raises(InputError):
        user_profile_sethandle(token1, 'alen')

    with pytest.raises(InputError):
        user_profile_sethandle(token1, 'a')

    with pytest.raises(InputError):
        user_profile_sethandle(token1, '123456789123456789123')

def test_user_all():
    reset_all()
    data1 = auth_register('123456789@gmail.com', 'password', 'jiahao', 'zhang')
    token1 = data1['token']
    u_id1 = data1['u_id']
    assert users_all(token1) == [{
        'u_id': u_id1,
        'email': '123456789@gmail.com',
        'name_first': 'jiahao',
        'name_last': 'zhang',
        'handle_str': 'jiahaozhang',
    }]
