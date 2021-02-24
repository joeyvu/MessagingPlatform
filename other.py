# pylint: disable=missing-docstring
# pylint: disable=import-error

'''Contains other routes for server. This includes
/admin/userpermission/change, standup/start, standup/send, standup/active,
/search and workspace/reset'''

from json import dumps
from flask import Blueprint, request
from other_functions import user_permission, standup_start, \
    standup_active, standup_send, workspace_reset, search

OTHER = Blueprint('other', __name__)

@OTHER.route('/admin/userpermission/change', methods=['POST'])
def change_permission():
    data = request.get_json()
    return dumps(user_permission(data["token"], data["u_id"], data["permission_id"]))

@OTHER.route('/standup/start', methods=['POST'])
def start_standup():
    data = request.get_json()
    return dumps(standup_start(data["token"], data["channel_id"], data["length"]))

@OTHER.route('/standup/active', methods=['GET'])
def active_standup():
    token = request.args.get("token")
    channel_id = request.args.get("channel_id")
    return dumps(standup_active(token, channel_id))

@OTHER.route('/standup/send', methods=['POST'])
def send_standup():
    data = request.get_json()
    return dumps(standup_send(data["token"], data["channel_id"], data["message"]))

@OTHER.route('/workspace/reset', methods=['POST'])
def reset_workspace():
    return dumps(workspace_reset())

@OTHER.route('/search', methods=['GET'])
def search_function():
    token = request.args.get('token')
    message = request.args.get('query_str')
    return dumps(search(token, message))
