'''user.py contains routes for user_functions.'''
from json import dumps
from flask import Blueprint, request
from user_functions import user_profile_setname, user_profile_setemail, user_profile_sethandle, \
    user_profile, users_all, user_upload_photo, user_remove

USER = Blueprint('user', __name__)

@USER.route('/user/profile/setname', methods=['PUT'])
def setname():
    '''Sets the input name from a user to their profile.'''
    details = request.get_json()
    return dumps(user_profile_setname(details['token'], details['name_first'], \
        details['name_last']))

@USER.route('/user/profile/setemail', methods=['PUT'])
def setemail():
    '''Sets the input email of a user to their profile.'''
    details = request.get_json()
    return dumps(user_profile_setemail(details['token'], details['email']))

@USER.route('/user/profile/sethandle', methods=['PUT'])
def sethandle():
    '''Sets the input handle of a user to their profile.'''
    details = request.get_json()
    return dumps(user_profile_sethandle(details['token'], details['handle_str']))

@USER.route('/user/profile', methods=['GET'])
def view_profile():
    '''Returns information about a valid user.'''
    token = request.args.get("token")
    u_id = request.args.get("u_id")
    return dumps(user_profile(token, u_id))

@USER.route('/users/all', methods=['GET'])
def all_profiles():
    '''Returns information about a valid user.'''
    token = request.args.get('token')
    return dumps(users_all(token))

@USER.route('/user/profile/uploadphoto', methods=['POST'])
def photo_upload():
    '''Receives a URL of an image on the internet, crops the
    image within bounds and sets as the user's profile picture.'''
    details = request.get_json()
    x_start = int(details["x_start"])
    y_start = int(details["y_start"])
    x_end = int(details["x_end"])
    y_end = int(details["y_end"])
    return dumps(user_upload_photo(details["token"], details["img_url"],\
        x_start, y_start, x_end, y_end))

@USER.route('/admin/user/remove', methods=['DELETE'])        
def remove_user():
    '''Remove the user from slackr'''
    token = request.args.get("token")
    u_id = request.args.get("u_id")
    return dumps(user_remove(token, u_id))