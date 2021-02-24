# pylint: disable=import-error
# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=redefined-outer-name
'''File contains all functions for other routes.'''
import json
import time
from auth_helper import find_token
from error import InputError, AccessError
from  message_functions import message_send

def get_data():
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)
    return database

def store_data(database):
    with open('data_store.json', 'w') as FILE:
        json.dump(database, FILE)


def check_token(token):
    email = find_token(token)
    database = get_data()
    if email is None:
        raise AccessError(description='Invalid token')
    else:
        # Check if a decoded token belongs to an existing user
        for user in database["users"]:
            if user["email"] == email:
                return email
        raise AccessError(description='Invalid token')

def find_channel(data, channel_id):
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            return i
    return None

def reset_all():
    database = get_data()
    database['users'].clear()
    database['channels'].clear()
    if 'stand_up_message' in database:
        database['stand_up_message'].clear()
    with open('data_store.json', 'w') as FILE:
        json.dump(database, FILE)


def user_permission(token, u_id, permission_id):
    '''Sets a user's permissions to new permission_id.'''
    database = get_data()
    # checks if the token given is valid
    email = check_token(token)
    check_user = False
    valid_ids = [1, 2]
    if permission_id not in valid_ids:
        raise InputError('Invalid permission_id')

    # checks if u_id and token refers to a valid user
    for user in database["users"]:
        if user["email"] == email:
            if user["permissions"]["global"] == 2:
                raise AccessError(description='User is not an owner')
        if user["u_id"] == u_id:
            user["permissions"]["global"] = permission_id
            store_data(database)
            return {}
    raise InputError(description='u_id does not refer to a valid user')


def standup_start(token, channel_id, length):
    '''Starts a standup in a channel.'''
    database = get_data()
    database['standup_messages'] = [] ## set up a message list for stand up message
    email = find_token(token)
    for user in database["users"]:
        if user["email"] == email:
            check_token = True
    if check_token is False:
        raise AccessError(description='Invalid token')

    channel = find_channel(database, channel_id)
    if channel is None:  # check standup start condition
        raise InputError(description='channel id is not a valid channel')
    if channel['standup_active']:
        raise InputError(description='standup is currently running in channel')

    time_start = time.time()
    channel['standup_active'] = time_start + length # save as time, otherwise none
    while time.time() < time_start + length:
        pass          # stand_up/send message will be add into database['standup_messages']


    channel['standup_active'] = None
    for i in database['standup_messages']:
        message_send(token, channel_id, i)


    database['standup_messages'].clear() # clear standup messages after standup is end
    store_data(database)
    return {time_start + length}

def standup_active(token, channel_id):
    '''Checks if a channel currently has an active standup.'''
    database = get_data()
    email = find_token(token)
    for user in database["users"]:
        if user["email"] == email:
            check_token = True
    if check_token is False:
        raise AccessError(description='Invalid token')
    channel = find_channel(database, channel_id)
    if channel is None:  # check valid channel_id
        raise InputError(description='channel_id is not a valid channel')

    if "standup_active" not in channel: # no saved time, there is no current standup session
        is_active = False
        time_finish = None
    else:
        time_finish = channel['standup_active'] # set time_finished as saved time
        is_active = True
    return {
        "is_active" : is_active,
        "time_finish" : time_finish
    }

def standup_send(token, channel_id, message):
    '''A function to send a message and packages it into one whole message under standup.'''
    database = get_data()
    email = find_token(token)
    for user in database["users"]: # check if token is valid
        if user["email"] == email:
            check_token = True
    if check_token is False:
        raise AccessError(description='Invalid token')

    channel = find_channel(database, channel_id)
    if channel is None:  # check valid channel_id
        raise InputError(description='channel_id is not a valid channel')

    if channel["standup_active"] is None:
        raise InputError(description='No current active standup in channel')

    if len(message) > 1000:
        raise InputError(description='Message cannot be over 1000 characters long')

    for user in database["users"]:
        if user["email"] == email:
            if user["u_id"] not in channel["all_members"]:
                raise AccessError(description='user is not a member of the channel')

    database["standup_messages"].append(message) # add to list of messages in that channel
    return {}

def workspace_reset():
    '''Clears all data from workspace to a new state.'''
    database = get_data()
    database['users'].clear()
    database['channels'].clear()
    if 'stand_up_message' in database:
        database['stand_up_message'].clear()
    with open('data_store.json', 'w') as FILE:
        json.dump(database, FILE)
    return {}

def search(token, message):
    '''
    Given a query string, return a collection of messages in all of the
    channels that the user has joined that match the query.
    '''
    message_list = []
    u_id = None

    database = get_data()

    #Find user email from token
    email = find_token(token)

    #Find u_id from email
    for user in database['users']:
        if user['email'] == email:
            u_id = user['u_id']

    #Find matching message and u_id and add to list
    for i in database["channels"]:
        if u_id in i['members']:
            for all_message in i['messages']:
                if u_id == all_message['u_id']:
                    if message in all_message['message']:
                        message_list.append(all_message)

    message_list.reverse()
    return {
        "messages" : message_list
    }