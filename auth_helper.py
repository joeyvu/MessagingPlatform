'''File containing all helper functions for auth'''
import re
import hashlib
import jwt
import secrets
import string
import smtplib
import ssl

SECRET = 'newslackr'

def check_valid_email(email):
    '''Checks if input is a valid email address.'''
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return bool(re.search(regex, email))

def check_unused_email(email, data):
    '''Checks if email has been registered before.'''
    for user in data:
        if user["email"] == email:
            return False
    return True

def hash_password(password):
    '''Returns a hash of a password.'''
    return hashlib.sha256(password.encode()).hexdigest()

def check_name(name):
    '''Checks if name is between 1 and 50 characters long.'''
    if len(name) >= 1 and len(name) <= 50:
        return True
    return False

def create_handle(name_first, name_last):
    '''Generates a handle that is the concatenation of
    a lowercase only first name and last name.'''
    handle_str = name_first.lower() + name_last.lower()
    if len(handle_str) > 20:            # if the concatenation is longer than 20 characters,
        handle_str = handle_str[:20]    # it is cutoff at 20 characters
    return handle_str

def generate_token(email):
    '''Generates a token.'''
    encoded = jwt.encode({"email": email}, SECRET, algorithm='HS256').decode('utf-8')
    return encoded

def find_token(token):
    '''Decodes a token and returns the email of the token.'''
    decoded = jwt.decode(token.encode('utf-8'), SECRET, algorithms=['HS256'])
    return decoded["email"]

def temporary_code():
    '''Creates a 10 character alphanumeric code for password reset.'''
    alphabet = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(10)) 
    return code

def send_email(receiver, code):
    '''Uses gmail SMTP and SSL connection to send recovery code to reset passwords.'''
    sender = "slackr4bc@gmail.com"  # Account to send emails
    sender_password = "4BrainCells!"

    subject = "Recovery code for Slackr account"
    body = f"Hello,\n"\
        "You have recently requested to reset your password for your slackr account.\n"\
        f"Your reset code is {code}"

    message = f"Subject: {subject}\n"\
            f"To: {receiver}\n"\
            f"From: {sender}\n"\
            f"{body}"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as mail:
        mail.ehlo()
        mail.login(sender, sender_password)
        mail.sendmail(sender, receiver, message)
    return
