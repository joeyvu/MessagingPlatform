'''auth.py contains routes for auth_functions'''
from json import dumps
from flask import Blueprint, request
from auth_functions import auth_login, auth_logout, auth_register,\
    auth_passwordreset_request, auth_passwordreset_reset

AUTH = Blueprint('auth', __name__)

@AUTH.route('/auth/register', methods=['POST'])
def register():
    '''Registers a user with their email, password, first name and last name.'''
    details = request.get_json()
    return dumps(auth_register(details["email"], details["password"],\
        details["name_first"], details["name_last"]))

@AUTH.route('/auth/login', methods=['POST'])
def login():
    '''Logs in a user with their email and password.'''
    details = request.get_json()
    return dumps(auth_login(details["email"], details["password"]))

@AUTH.route('/auth/logout', methods=['POST'])
def logout():
    '''Logs out a user with their token.'''
    details = request.get_json()
    return dumps(auth_logout(details["token"]))

@AUTH.route('/auth/passwordreset/request', methods=['POST'])
def password_request():
    '''Sends a reset code to the given email to reset a password.'''
    details = request.get_json()
    return dumps(auth_passwordreset_request(details["email"]))

@AUTH.route('/auth/passwordreset/reset', methods=['POST'])
def password_reset():
    '''Resets a password after giving a correct reset code.'''
    details = request.get_json()
    return dumps(auth_passwordreset_reset(details["reset_code"], details["new_password"]))
