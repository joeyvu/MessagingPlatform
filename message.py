# pylint: disable=W0105
# pylint: disable=W0614

'''message.py has routes for message functions'''
from json import dumps
import random
import requests
from flask import Blueprint, request
from message_functions import message_remove, message_edit,\
 message_react, message_unreact, message_send, message_pin, message_unpin
from hangman_helper import censor, guess_sep, check

'''
from datetime import timezone
import uuid
from datetime import timezone
'''

MESSAGE = Blueprint('message', __name__)

HANGMAN_PLAY = 0
TRACKER = 0
SINGLE_WORD = None
CENSORED = None
GUESSES = []

@MESSAGE.route('/message/remove', methods=['DELETE'])
def remove():
    '''Removes a message with the user's token and message id'''
    details = request.get_json()
    return dumps(message_remove(details["token"], details["message_id"]))

@MESSAGE.route('/message/edit', methods=['PUT'])
def edit():
    '''Edits a message with the user's token and message id'''
    details = request.get_json()
    return dumps(message_edit(details['token'], details['message_id'], details['message']))

@MESSAGE.route('/message/react', methods=['POST'])
def react():
    '''Reacts a message by giving a react id from the user's token and message id'''
    details = request.get_json()
    return dumps(message_react(details['token'], details['channel_id'], details['react_id']))

@MESSAGE.route('/message/unreact', methods=['POST'])
def unreact():
    '''Unreacts a message by removing the react id from the user's token and message id'''
    details = request.get_json()
    return dumps(message_unreact(details['token'], details['channel_id'], details['react_id']))


@MESSAGE.route("/message/send", methods=["POST"])
def send():
    '''Function sends a message and plays hangman when /hangman is entered'''
    data = request.get_json()
    global HANGMAN_PLAY, TRACKER, CENSORED, SINGLE_WORD, GUESSES

    if HANGMAN_PLAY == 1 and data["message"].startswith('/guess'):
        guess = guess_sep(data["message"])
        checked = check(guess[1], SINGLE_WORD, CENSORED)
        if guess[0] == 0: #/guess entered but not properly. e.g /guess or /guessX
            message = "Please type in guess correctly"
        elif guess[0] == 1: #No space provided after guess
            message = "No space provided after /guess"
        elif guess[0] == 2: #Guess entered correctly
            if checked[0] == 2:
                message = "You won! The word was " + SINGLE_WORD
                HANGMAN_PLAY = 0
                TRACKER = 0
                GUESSES = []
            elif checked[0] == 1: #Correct guess. Reveal word
                message = checked[1]
                CENSORED = checked[1]
                if SINGLE_WORD == message:
                    message = "You won! The word was " + SINGLE_WORD
                    HANGMAN_PLAY = 0
                    TRACKER = 0
                    GUESSES = []
            elif checked[0] == 0: #Wrong guess
                if guess[1] not in GUESSES:
                    GUESSES.append(guess[1])
                TRACKER += 1
                message = "Wrong guess. Try again! You have " + str(9 - TRACKER)\
                + " lives left and have guessed " + str(GUESSES) + " so far!"
                if 9 - TRACKER == 1:
                    message = "Wrong guess. Try again! You have " + str(9 - TRACKER)\
                    + " life left and have guessed " + str(GUESSES) + " so far!"
                if TRACKER >= 9:
                    message = "You ran out of lives. Game over :( The word was " + SINGLE_WORD
                    HANGMAN_PLAY = 0
                    TRACKER = 0
                    GUESSES = []
        return dumps(message_send(data["token"], data["channel_id"], message))

    if data["message"] == "/hangman" and HANGMAN_PLAY == 0:
        HANGMAN_PLAY = 1

        site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        response = requests.get(site)
        SINGLE_WORD = str(random.choice(response.content.splitlines()).decode("utf-8"))
        SINGLE_WORD = SINGLE_WORD.lower()

        CENSORED = censor(SINGLE_WORD)
        message = "Hangman game has begun! You have 9 lives, goodluck! Try to guess " + CENSORED
        return dumps(message_send(data["token"], data["channel_id"], message))

    return dumps(message_send(data["token"], data["channel_id"], data["message"]))

@MESSAGE.route("/message/sendlater", methods=["POST"])
def send_later():
    '''Sends a message after a given time. Does not work'''
    data = request.get_json()
    return dumps(message_send(data["token"], data["channel_id"], data["message"]))


@MESSAGE.route("/message/pin", methods=["POST"])
def pin():
    '''Pin message'''
    data = request.get_json()
    return dumps(message_pin(data["token"], data["message_id"]))

@MESSAGE.route("/message/unpin", methods=["POST"])
def unpin():
    '''Unpin message'''
    data = request.get_json()
    return dumps(message_unpin(data["token"], data["message_id"]))
