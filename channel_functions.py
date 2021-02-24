# pylint: disable=invalid-name
# pylint: disable=import-error
# pylint: disable=too-many-nested-blocks
# pylint: disable=inconsistent-return-statements
# pylint: disable=redefined-outer-name
'''Channel functions created for channel.py'''

import json
from error import AccessError, InputError
from auth_helper import find_token

def get_data():
    '''Open the database for the server.'''
    with open('data_store.json', 'r') as file_inputs:
        database = json.load(file_inputs)
    return database

def get_profile(u_id):
    '''Receives a u_id and generates a profile.'''
    database = get_data()
    for user in database["users"]:
        if user["u_id"] == u_id:
            keys = ["email", "password", "handle_str", "permissions", "reset_code"]
            return {k : v for k, v in user.items()  if k not in keys}

def channel_invite(token, channel_id, u_id):
    '''Functions that invites user to channel'''

    database = get_data()

    # Find the channel dict with given channel id
    for channel in database["channels"]:
        if channel["channel_id"] == channel_id:
            # Finds user sending the invite from token
            email = find_token(token)
            for user_1 in database['users']:
                if user_1['email'] == email:
                    # Check if user1 is part of the channel
                    for member in channel["members"]:
                        if user_1["u_id"] == member:
                            # Finds the user invited from u_id
                            for user_2 in database['users']:
                                if user_2["u_id"] == u_id:
                                    # Adds user2 as a member of the channel
                                    channel["members"].append(u_id)
                                    with open('data_store.json', 'w') as FILE:
                                        json.dump(database, FILE)
                                    return {}
                            raise InputError(description='u_id does not refer to valid user')
                    raise InputError(description='User is not a member of the channel')
            raise AccessError(description='Invalid token')

def channel_join(token, channel_id):
    '''Given a channel_id, adds the authorised user to the channel'''
    database = get_data()
    # Find channel dict with given channel_id
    for channel in database["channels"]:
        if channel["channel_id"] == channel_id:
            # Check if channel is private
            if channel["is_public"]is False:
                raise AccessError(description="Channel is private")
            # Find user from token
            email = find_token(token)
            for user in database["users"]:
                if user["email"] == email:
                    for member in channel["members"]:
                        if user["u_id"] == member:
                            raise InputError(description='User is already a member of the channel')
                    channel["members"].append(user["u_id"])
                    with open('data_store.json', 'w') as FILE:
                        json.dump(database, FILE)
                    return {}
            raise AccessError(description="Invalid token")
    raise InputError(description="Invalid channel_id")

def channel_leave(token, channel_id):
    '''Given a channel ID, the user removed as a member of this channel.'''
    database = get_data()
    # Find channel dict with given channel_id
    for channel in database["channels"]:
        if channel["channel_id"] == channel_id:
            # Find user from token
            email = find_token(token)
            for user in database["users"]:
                if user["email"] == email:
                    # Check if user is in channel
                    for member in channel["members"]:
                        if member == user["u_id"]:
                            channel["members"].remove(user["u_id"])
                            with open('data_store.json', 'w') as FILE:
                                json.dump(database, FILE)
                            return {}
                    raise AccessError(description="User is not a member of the channel")
            raise AccessError(description="Invalid token")
    raise InputError(description="Invalid channel_id")

def channel_details(token, channel_id):
    '''Function that returns the details of channel'''
    database = get_data()
    email = find_token(token)
    for user in database["users"]:
        if user["email"] == email:
            # Find channel dict with given channel_id
            for channel in database["channels"]:
                if channel["channel_id"] == channel_id:
                    owner_members = []
                    for owner in channel["owners"]:
                        owner_dict = get_profile(owner)
                        owner_members.append(owner_dict)
                    all_members = []
                    for member in channel["members"]:
                        member_dict = get_profile(member)
                        all_members.append(member_dict)
                    return {
                        "name" : channel["name"],
                        "owner_members" : owner_members,
                        "all_members" : all_members
                    }
    raise AccessError(description="Invalid token")

def channel_messages(token, channel_id, start):
    '''Function that shows up to 50 messages based on the start value'''
    database = get_data()
    # Find channel dict with given channel_id
    for channel in database['channels']:
        if channel['channel_id'] == channel_id:
            #Find user from token
            email = find_token(token)
            for user_1 in database['users']:
                if user_1['email'] == email:
                    #Check if user is member of channel
                    for member in channel['members']:
                        if member == user_1['u_id']:
                            #Find total number of messages
                            messages_total = len(channel['messages'])
                            #Check for empty list
                            if not channel["messages"]:
                                return {"messages" : [], "start" : start, "end" : -1}
                            #Start value is bigger than total number of messages
                            start = int(start)
                            if start > messages_total:
                                raise InputError(description='Start value is too big')

                            recent_messages = []
                            end = start + 50
                            #Runs through up to 50 messages
                            if end > messages_total: #Less than 50 messages left to load
                                end = messages_total
                                while end > start: #Starts from end of messages to start value
                                    recent_messages.append(channel['messages'][end-1])
                                    end -= 1
                                return {"messages" : recent_messages, "start" : start, "end" : -1}
                            while end > start:
                                #Last message will be first message returned
                                recent_messages.append(channel['messages'][end-1])
                                end -= 1
                            return {
                                "messages" : recent_messages,
                                "start" : start,
                                "end" : start + 50
                                }
                    raise AccessError(description="User is not a member of the channel")
            raise AccessError(description="Invalid token")
    raise InputError(description="Invalid channel_id")

def channel_addowner(token, channel_id, u_id):
    '''Turns the user with given u_id into an owner of the channel'''
    database = get_data()
    # Find channel dict with given channel_id
    for channel in database['channels']:
        if channel['channel_id'] == channel_id:
            #Find user from token
            email = find_token(token)
            for user_1 in database['users']:
                if user_1['email'] == email:
                    #Check if authorised user is an owner
                    for owner in channel['owners']:
                        if owner == user_1['u_id']:
                            #Check if other user is owner as well
                            for owner in channel['owners']:
                                if owner == u_id: #u_id is given input from function
                                    raise InputError(description='User is already owner of channel')
                            channel['owners'].append(u_id) #Adds user as owner if user is not owner
                            with open('data_store.json', 'w') as FILE:
                                json.dump(database, FILE)
                            return {}
                    raise AccessError(description='User is not owner of channel')
            raise AccessError(description="Invalid token")
    raise InputError(description="Invalid channel_id")

def channel_removeowner(token, channel_id, u_id):
    '''Removes user with given u_id from the list of owners in that channel'''
    database = get_data()
    # Find channel dict with given channel_id
    for channel in database['channels']:
        if channel['channel_id'] == channel_id:
            #Find user from token
            email = find_token(token)
            for user_1 in database['users']:
                if user_1['email'] == email:
                    #Check if authorised user is an owner
                    for owner in channel['owners']:
                        if owner == user_1['u_id']:
                            for owner in channel['owners']:
                                if owner == u_id: #u_id is given input from function
                                    channel['owners'].remove(u_id)
                                with open('data_store.json', 'w') as FILE:
                                    json.dump(database, FILE)
                                return {}
                            raise InputError(description='User is not owner of channel')
                    raise AccessError(description='Authorised user is not owner of channel')
            raise AccessError(description="Invalid token")
    raise InputError(description="Invalid channel_id")
