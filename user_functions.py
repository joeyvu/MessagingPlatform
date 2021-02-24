'''Contains implementations for user endpoints.'''
# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=pointless-string-statement
import re
import json
import urllib
from auth_helper import find_token, temporary_code
from channel_functions import channel_removeowner
from message_functions import message_remove
from error import InputError, AccessError
from PIL import Image
from io import BytesIO
from flask import url_for

'''Helper functions.'''

def get_data():
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)
    return database

def check_handle(handle_str):
    database = get_data()
    flag = True
    for user in database["users"]:
        if user["handle_str"] == handle_str:
            flag = False
    if flag is False:
        raise InputError(description='Invalid handle')
    if len(handle_str) < 2 or len(handle_str) >= 20:
        raise InputError(description='Invalid handle')


def check_email(email):
    database = get_data()
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    flag = bool(re.search(regex, email))
    for user in database['users']:
        if user["email"] == email:
            flag = False
    if flag is False:
        raise InputError(description='Invalid email')


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


def give_profile(user): # Receives a user dict and only returns keys visible on frontend
    keys = ["password", "permissions", "reset_code", "channels"]
    return {k : v for k, v in user.items()  if k not in keys}

def reset_all():
    database = get_data()
    database['users'].clear()
    with open('data_store.json', 'w') as FILE:
        json.dump(database, FILE)

'''Core functions'''

def user_profile_setname(token, name_first, name_last):
    email = check_token(token)

    if len(name_first) < 2 or len(name_first) > 49:
        raise InputError(description='Invalid name_first')

    if len(name_last) < 2 or len(name_last) > 49:
        raise InputError(description='Invalid name_last')

    database = get_data()
    # Check if a decoded token belongs to an existing user and sets their name
    for user in database["users"]:
        if user["email"] == email:
            user["name_first"] = name_first
            user["name_last"] = name_last
            with open('data_store.json', 'w') as FILE:
                json.dump(database, FILE)

    return {}

def user_profile_setemail(token, email):
    old_email = check_token(token)
    check_email(email)
    database = get_data()
    # Check if a decoded token belongs to an existing user and sets their email
    for user in database["users"]:
        if user["email"] == old_email:
            user["email"] = email
            with open('data_store.json', 'w') as FILE:
                json.dump(database, FILE)
    return {}

def user_profile_sethandle(token, handle_str):
    email = check_token(token)

    check_handle(handle_str)
    database = get_data()

    # Check if a decoded token belongs to an existing user and sets their handle
    for user in database["users"]:
        if user["email"] == email:
            user["handle_str"] = handle_str
            with open('data_store.json', 'w') as FILE:
                json.dump(database, FILE)
    return {}

def user_profile(token, u_id):
    email = check_token(token)
    database = get_data()
    # Checks given u_id for valid user in database and returns a profile
    for user in database["users"]:
        if user["u_id"] == u_id:
            user_dict = give_profile(user)
            return {
                    "user" : user_dict
                    }
    raise InputError(description='Invalid u_id')

def users_all(token):
    email = check_token(token)
    database = get_data()
    all_users = []
    # Returns all users with their associated details in slackr
    for user in database["users"]:
        user_dict = give_profile(user)
        all_users.append(user_dict)

    return {
            "users" : all_users
            }

def user_upload_photo(token, img_url, x_start, y_start, x_end, y_end):
    '''Crops an image from a URL and sets as user profile picture.'''
    database = get_data()

    # Find user from token
    email = find_token(token)
    for user in database["users"]:
        if user["email"] == email:
            # Save image from img_url into static folder
            # and check that it returns a HTTP status of 200
            try:
                local_filename, headers = urllib.request.urlretrieve(img_url)
            except urllib.error.HTTPError:
                raise ValueError("img_url returns HTTP status other than 200")

            # Check if image is jpg type
            if headers["Content-Type"] not in ["image/jpeg", "image/jpg"]:
                raise ValueError("Image uploaded is not a JPG")

            # Open the image in static folder
            with Image.open(local_filename) as img:
                # Check if crop dimensions are within bounds of the image size
                width, height = img.size
                if x_start < 0 or y_start < 0 or \
                    x_start > width or y_start > height:
                    raise ValueError("Index not within the dimensions of the image")
                if x_end > width or y_end > width or \
                    x_end < x_start or y_end < y_start:
                    raise ValueError("Index not within the dimensions of the image")

                # Crop the image
                box = (x_start, y_start, x_end, y_end)
                cropped_img = img.crop(box)
                file_name = temporary_code()
                cropped_img.save("static/" + file_name + ".jpg")
            # Set the new url to user's profile_img_url e.g. /static/filename.jpg
            new_url = url_for("static", filename = file_name + ".jpg", _external = True)
            user["profile_img_url"] = new_url
            with open('data_store.json', 'w') as FILE:
                json.dump(database, FILE)
            return {}

def user_remove(token, u_id):
    email = check_token(token)
    database = get_data()
    for user in database["users"]:
        if user["email"] == email:
            if user["permissions"]["global"] != 1:
                raise AccessError(description='Given token is not from owner')
    for user in database["users"]:
        if user["u_id"] == u_id:
            for channel in database["channels"]:
                if u_id in channel["members"]:
                    for message in channel['messages']:
                        if message['u_id'] == u_id:
                            message_remove(token, message['message_id'])
                if u_id in channel['owners']:
                    channel_removeowner(token, channel['channel_id'], u_id)
                elif u_id in channel["members"]:
                    channel["members"].remove(u_id)
            database["users"].remove(user)
            with open('data_store.json', 'w') as FILE:
                json.dump(database, FILE)
            return {}
    raise InputError(description='Invalid u_id')