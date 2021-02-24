'''Message functions created for message.py'''

import uuid
import json
from datetime import datetime
from error import InputError, AccessError
from auth_helper import find_token

def channel_checker(channel_id):
    '''Checks if the channel_id is valid'''
    verify_channel = 0
    channel_info = None

    #Open database
    with open('data_store.json', 'r') as file_inputss:
        database = json.load(file_inputss)

    #Checks if the channel id is valid
    for channel in database['channels']:
        if channel['channel_id'] == channel_id:
            verify_channel = 1
            channel_info = channel

    if verify_channel == 0:
        raise InputError(description='Invalid channel id')

    return channel_info

def message_remove(token, message_id):
    '''Function to remove message'''
    verify_owner = 0
    verify_message = 0
    current_message = []
    current_channel = []
    u_id = None

    #Opens database
    with open('data_store.json', 'r') as file_input_two:
        database = json.load(file_input_two)

    #Goes through token verification and returns user id
    u_id = token_verification(token)

    #Find message from database
    for channel in database['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                verify_message = 1
                current_channel.append(channel)
                current_message.append(message)

    #If message_id does not exist
    if verify_message == 0:
        raise InputError(description='Message no longer exists')

    #Verify authorised user's id with u_id
    if current_message[0]['u_id'] != u_id:
        raise AccessError('Message request was not sent by authorised user')

    #Check if user is owner of channel
    for owner in current_channel[0]['owners']:
        if owner == u_id:
            verify_owner = 1

    if verify_owner == 0:
        raise AccessError(description="Authorised user is not owner")

    #Function that removes the message from list of messages
    current_channel[0]['messages'].remove(current_message[0])

    with open('data_store.json', 'w') as file_input_three:
        json.dump(database, file_input_three)
    return {}

def message_edit(token, message_id, message):
    '''Function to edit message'''
    new_message = message
    verify_owner = 0
    verify_message = 0
    u_id = None
    current_message = []
    current_channel = []

    #Opens database
    with open('data_store.json', 'r') as file_input_four:
        database = json.load(file_input_four)

    #Goes through token verification and returns user id
    u_id = token_verification(token)

    #Find message from database
    for channel in database['channels']:
        for msg in channel['messages']:
            if msg['message_id'] == message_id:
                verify_message = 1
                current_channel.append(channel)
                current_message.append(msg)

    #If message_id does not exist
    if verify_message == 0:
        raise InputError(description='Message no longer exists')

    #Verify authorised user's id with u_id
    if current_message[0]['u_id'] != u_id:
        raise AccessError('Message request was not sent by authorised user')

    #Check if user is owner of channel
    for owner in current_channel[0]['owners']:
        if owner == u_id:
            verify_owner = 1

    if verify_owner == 0:
        raise AccessError(description="Authorised user is not owner")

    #Function to edit message
    if new_message == '':
        message_remove(token, message_id)
    else:
        current_message[0]['message'] = new_message

    with open('data_store.json', 'w') as file_input_five:
        json.dump(database, file_input_five)
    return {}

def message_react(token, message_id, react_id):
    '''Function to react message'''
    verify_message = 0
    u_id = None
    current_message = []

    #Opens database
    with open('data_store.json', 'r') as file_input_six:
        database = json.load(file_input_six)

    #Goes through token verification and returns user id
    u_id = token_verification(token)

    #Find message from database
    for channel in database['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                verify_message = 1
                current_message.append(message)

    #If message_id does not exist
    if verify_message == 0:
        raise InputError(description="Message_id is not valid")

    #Check if react_id is valid
    if current_message[0]['reacts'][0]['react_id'] != react_id:
        raise InputError(description='react_id is not a valid React ID')

    #Checks if user has reacted to message
    if current_message[0]['reacts'][0]['is_this_user_reacted'] is True:
        raise InputError(description='The message is already reacted')

    #Function to react to message
    current_message[0]['reacts'][0]['u_ids'].append(u_id)
    current_message[0]['reacts'][0]['is_this_user_reacted'] = True

    with open('data_store.json', 'w') as file_input_seven:
        json.dump(database, file_input_seven)
    return {}

def message_unreact(token, message_id, react_id):
    '''Function to unreact message'''
    verify_message = 0
    u_id = None
    current_message = []

    #Opens database
    with open('data_store.json', 'r') as file_input_eight:
        database = json.load(file_input_eight)

    #Goes through token verification and returns user id
    u_id = token_verification(token)

    #Find message from database
    for channel in database['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                verify_message = 1
                current_message.append(message)

    #If message_id does not exist
    if verify_message == 0:
        raise InputError(description="Message_id is not valid")

    #Check if react_id is valid
    if current_message[0]['reacts'][0]['react_id'] != react_id:
        raise InputError(description='react_id is not a valid React ID')

    #Checks if user has reacted to message
    if current_message[0]['reacts'][0]['is_this_user_reacted'] is False:
        raise InputError(description='The message is not reacted')

    #Function to unreact to message
    current_message[0]['reacts'][0]['u_ids'].remove(u_id)
    current_message[0]['reacts'][0]['is_this_user_reacted'] = False

    with open('data_store.json', 'w') as file_input_nine:
        json.dump(database, file_input_nine)
    return {}

def message_send(token, channel_id, message):
#Send a message from authorised_user to the channel specified by channel_id

    with open('data_store.json', 'r') as FILE:
        database = json.load(FILE)

    #Check if lenght of string is <1000
    if len(message) > 1000:
        raise InputError(description = 'Message length greater than 1000.')

    email = find_token(token)
    for user in database["users"]:
        if user["email"] == email:
            for channel in database["channels"]:
                if channel["channel_id"] == channel_id:
                    for member in channel["members"]:
                        if member == user["u_id"]:
                            timestamp = datetime.now().timestamp()
                            message_id = uuid.uuid4().int
                            text = {
                                "message_id" : message_id,
                                "u_id" : user["u_id"],
                                "message" : message,
                                "time_created" : timestamp,
                                "reacts" : [],
                                "is_pinned" : False 
                            }
                            channel["messages"].append(text)
                            with open('data_store.json', 'w') as FILE:
                                json.dump(database, FILE)
                            return {
                                "message_id" : message_id
                            }
                    raise AccessError(description = 'User is not a memmber of the channel')
    raise AccessError(description = 'Invalid token')

def message_pin(token, message_id):
    '''Function to pin a message'''
    u_id = None
    verify_message = 0
    verify_owner = 0
    current_message = []
    current_channel = []

    #Open database
    with open('data_store.json', 'r') as file_input_twelve:
        database = json.load(file_input_twelve)

    #Goes through token verification and returns user id
    u_id = token_verification(token)

    #Check if message_id is valid
    for channel in database['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                verify_message = 1
                current_message.append(message)
                current_channel.append(channel)

    if verify_message == 0:
        raise InputError(description='Invalid message id')

    #Check if user is member of channel by checking u_id in message
    if current_message[0]['u_id'] != u_id:
        raise AccessError(description='User is not a member of the channel')

    #Check if user is owner of channel
    for owner in current_channel[0]['owners']:
        if owner == u_id:
            verify_owner = 1

    if verify_owner == 0:
        raise InputError(description='User is not owner')

    #Check if message is pinned and if unpinned, message will be pinned
    if current_message[0]['is_pinned'] is True:
        raise InputError(description='Message already pinned')

    current_message[0]['is_pinned'] = True
    assert current_message[0]['is_pinned'] is True

    with open('data_store.json', 'w') as file_input_thirteen:
        json.dump(database, file_input_thirteen)
    return {}

def message_unpin(token, message_id):
    '''Function to unpin a message'''
    u_id = None
    verify_message = 0
    verify_owner = 0
    current_message = []
    current_channel = []

    #Open database
    with open('data_store.json', 'r') as file_input_fourteen:
        database = json.load(file_input_fourteen)

    #Goes through token verification and returns user id
    u_id = token_verification(token)

    #Check if message_id is valid
    for channel in database['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                verify_message = 1
                current_message.append(message)
                current_channel.append(channel)

    if verify_message == 0:
        raise InputError(description='Invalid message id')

    #Check if user is member of channel by checking u_id in message
    if current_message[0]['u_id'] != u_id:
        raise AccessError(description='User is not a member of the channel')

    #Check if user is owner of channel
    for owner in current_channel[0]['owners']:
        if owner == u_id:
            verify_owner = 1

    if verify_owner == 0:
        raise InputError(description='User is not owner')

    #Check if message is unpinned and if pinned, message will be pinned
    if current_message[0]['is_pinned'] is False:
        raise InputError(description='Message already unpinned')

    current_message[0]['is_pinned'] = False
    assert current_message[0]['is_pinned'] is False

    with open('data_store.json', 'w') as file_input_fifteen:
        json.dump(database, file_input_fifteen)
    return {}
