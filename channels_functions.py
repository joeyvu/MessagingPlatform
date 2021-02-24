# pylint: disable=invalid-name
# pylint: disable=import-error
'''Channels functions for channels.py'''

import json
import uuid
from auth_helper import find_token
from error import InputError, AccessError

def give_channel(channel):
    '''Receives a channel dict and only returns keys visible on frontend.'''
    keys = ["is_public", "members", "owners", "messages"]
    return {k : v for k, v in channel.items()  if k not in keys}

def channels_list(token):
    '''Returns a list of channels the user is in.'''
    # Opens database
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)

    # Verifying Token
    email = find_token(token)
    for user in database["users"]:
        if user["email"] == email:
            all_channels = []
            for channel in database["channels"]:
                # Find all channels user is in
                if user["u_id"] in channel["members"]:
                    channel_dict = give_channel(channel)
                    all_channels.append(channel_dict)
            return {
                "channels" : all_channels
            }
    raise AccessError(description="Invalid token")

def channels_listall(token):
    '''Returns a list of all the channels in the slackr.'''
    # Opens database
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)

    # Verifying Token
    email = find_token(token)
    for user in database["users"]:
        if user["email"] == email:
            all_channels = []
            for channel in database["channels"]:
                # Get all channels in slackr
                channel_dict = give_channel(channel)
                all_channels.append(channel_dict)
            return {
                "channels" : all_channels
            }
    raise AccessError(description="Invalid token")

def channels_create(token, name, is_public):
    '''Creates a channel and assigns first user as owner.'''
    # Opens database
    with open('data_store.json', 'r') as FILE:
        database = json.load(FILE)
    # Find email from token
    email = find_token(token)
    for user in database["users"]:
        if user["email"] == email:
        #Checks the length of channel name
            if len(name) > 20:
                raise InputError(description='Name cannot be over 20 characters long')

            # Generate channel_id that is 5 digits long, convert to string
            new_id = uuid.uuid4().int
            channel_id = str(new_id)[:5]
            # Create new channel
            new_channel = {
                "channel_id" : channel_id,
                "name" : name,
                "is_public" : is_public,
                "members" : [user["u_id"]],
                "owners" : [user["u_id"]],
                "messages" : []
            }

            # Add channel to list of channels
            database["channels"].append(new_channel)
            with open('data_store.json', 'w') as FILE:
                json.dump(database, FILE)
            return {
                "channel_id" : new_channel["channel_id"]
            }
    raise AccessError(description="Invalid token")
