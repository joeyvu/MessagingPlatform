# pylint: disable=invalid-name
# pylint: disable=import-error

'''File containing all auth functions.'''
import uuid
import json
from error import InputError
from auth_helper import check_valid_email, check_unused_email,\
    check_name, hash_password, create_handle, generate_token, find_token,\
        temporary_code, send_email


def auth_register(email, password, name_first, name_last):
    '''Function to register a user.'''
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)
    # Conditions for inputs
    if check_valid_email(email) and check_unused_email(email, database['users']):
        if len(password) >= 6:
            if check_name(name_first) and check_name(name_last):
                new_id = uuid.uuid4().int
                u_id = str(new_id)[:11] # Make id 10 digits long, store as string
                token = generate_token(email)
                # Checks if the user is the first to sign up, assign as owner
                if database["users"] == []:
                    permission = 1
                else:
                    permission = 2
                # Generates user dict and writes to json file
                new_user = {
                    "u_id" : u_id,
                    "email" : email,
                    "name_first" : name_first,
                    "name_last" : name_last,
                    "handle_str" : create_handle(name_first, name_last),
                    "profile_img_url" : None,
                    "password" : hash_password(password),
                    "permissions" : {
                        "global" : permission,
                        "channels" : None
                    }
                }
                database['users'].append(new_user)
                with open('data_store.json', 'w') as FILE:
                    json.dump(database, FILE)
                return {
                    'u_id' : u_id,
                    'token' : token
                    }
            else:
                raise InputError(description='Names should be between 1-50 characters long')
        else:
            raise InputError(description='Password should be over 6 characters long')
    else:
        raise InputError(description='Email address is not valid/email is already registered')

def auth_login(email, password):
    '''Function to login a user.'''
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)
    # Get data from classes.py
    for user in database["users"]:   # Looks through list of users and finds email + password match
        if user["email"] == email:
            if user["password"] == hash_password(password):
                u_id = user["u_id"]
                token = generate_token(email)
                # Update database in json file
                with open('data_store.json', 'w') as FILE:
                    json.dump(database, FILE)
                return {
                    'u_id' : u_id,
                    'token' : token
                    }
    raise InputError(description='Email/Password is not correct')

def auth_logout(token):
    '''Function to logout a user.'''
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)
    # Check if token is valid
    email = find_token(token)
    for user in database["users"]:
        if user["email"] == email:
            return {'is_success' : True}
    return {'is_success' : False}

def auth_passwordreset_request(email):
    '''Sends a registered user an email containing a secret code
    to reset their password.'''
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)
    # Checks for existing user
    for user in database["users"]:
        if user["email"] == email:
            code = temporary_code() # Generate a secret code and send email
            user["reset_code"] = code
            send_email(email, code)
    with open('data_store.json', 'w') as FILE:  # Secret code is stored
        json.dump(database, FILE)
    return {}

def auth_passwordreset_reset(reset_code, new_password):
    '''Resets a user's password when given the correct code.'''
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)
    for user in database["users"]:
        reset = user.get("reset_code", None)    # Get reset code in user dict and compare
        if reset == reset_code:
            if len(new_password) < 6:
                raise InputError(description='Password should be over 6 characters long')
            user["password"] = hash_password(new_password)
            del user["reset_code"]
    with open('data_store.json', 'w') as FILE:  # New password is stored
        json.dump(database, FILE)
    return {}

def reset_data():
    '''Resets data for integration tests.'''
    with open("data_store.json", "r") as FILE:
        database = json.load(FILE)
        database["users"].clear()
        database["channels"].clear()
    with open("data_store.json", "w") as FILE:
        json.dump(database, FILE)
