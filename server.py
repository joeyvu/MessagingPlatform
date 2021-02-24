import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError

# Import blueprints here
from auth import AUTH
from user import USER
from other import OTHER
from message import MESSAGE
from channel import CHANNEL
from channels import CHANNELS

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

# Register blueprints here
APP.register_blueprint(AUTH)
APP.register_blueprint(USER)
APP.register_blueprint(OTHER)
APP.register_blueprint(MESSAGE)
APP.register_blueprint(CHANNEL)
APP.register_blueprint(CHANNELS)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
