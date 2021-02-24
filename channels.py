# pylint: disable=W0401
# pylint: disable=W0614

'''channels.py contains routes for channels_functions'''
from json import dumps
from flask import Blueprint, request
from channels_functions import *

CHANNELS = Blueprint('channels', __name__)

@CHANNELS.route('/channels/list', methods=['GET'])
def view_list():
    '''views the channel of the user'''
    return dumps(channels_list(request.args.get("token")))

@CHANNELS.route('/channels/listall', methods=['GET'])
def view_listall():
    '''views the whole list of channels'''
    return dumps(channels_listall(request.args.get("token")))

@CHANNELS.route('/channels/create', methods=['POST'])
def post_channels():
    '''creates a new channel'''
    details = request.get_json()
    return dumps(channels_create(details["token"], details["name"], details["is_public"]))
