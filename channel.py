# pylint: disable=redefined-outer-name
'''
channel.py has routes for channel functions
'''
from json import dumps
from flask import Blueprint, request
from channel_functions import channel_invite, channel_details, channel_join, channel_leave,\
    channel_messages, channel_addowner, channel_removeowner

CHANNEL = Blueprint('channel', __name__)

@CHANNEL.route('/channel/invite', methods=['POST'])
def invite():
    '''Invites a user to a channel'''
    details = request.get_json()
    return dumps(channel_invite(details['token'], details['channel_id'], details['u_id']))

@CHANNEL.route('/channel/details', methods=['GET'])
def details():
    '''Provides the details of a channel'''
    return dumps(channel_details(request.args.get('token'), request.args.get('channel_id')))

@CHANNEL.route('/channel/messages', methods=['GET'])
def messages():
    '''Provides up to 50 messages based on starting value'''
    return dumps(channel_messages(request.args.get('token'), request.args.get('channel_id'), \
        request.args.get('start')))

@CHANNEL.route('/channel/leave', methods=['POST'])
def leave():
    '''User remove itself as a member of the channel'''
    details = request.get_json()
    return dumps(channel_leave(details['token'], details['channel_id']))

@CHANNEL.route('/channel/join', methods=['POST'])
def join():
    '''Authorised user adds a new user to the channel'''
    details = request.get_json()
    return dumps(channel_join(details['token'], details['channel_id']))

@CHANNEL.route('/channel/addowner', methods=['POST'])
def addowner():
    '''User with u_id becomes an owner of the channel'''
    details = request.get_json()
    return dumps(channel_addowner(details['token'], details['channel_id'], details['u_id']))

@CHANNEL.route('/channel/removeowner', methods=['POST'])
def removeowner():
    '''Removes user with u_id as the owner of the channel'''
    details = request.get_json()
    return dumps(channel_removeowner(details['token'], details['channel_id'], details['u_id']))
