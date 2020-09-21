import smtplib, hashlib, os, re
#from flask_mail import Message, Mail
from email.message import EmailMessage
from cryptography.fernet import Fernet

def send_mail(to, subject, msg, frm = "Perilwise Onboard <onboard@perilwise.com>", html = None):
    '''
    Send email with the given message and details...

    Args:
    to      - the reciepient list (list input)
    subject - the subject of the email (string input)
    msg     - the message/body of the email (string input)
    frm     - the FROM address for the email, default is "onboard@perilwise.com"
    html    - the html content to include in the email (string input)
    '''
    mail = EmailMessage()
    mail.set_content("%s" % (msg))
    mail['Subject'] = subject
    mail['From'] = frm
    mail['To'] = to
    mail['Cc'] = cc
    if html:
        mail.add_alternative(html, subtype='html')
    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(mail)


def md5(str_inp):
    '''
    returns md5 hash hexadecimal value of the input string.

    Args:
    str_inp - the string input which is to be hashed
    '''
    return hashlib.md5(str_inp.encode()).hexdigest()

def validate_email(str_inp):
    '''
    validate input string if its a valid email ID

    Args:
    str_inp - the string to validate for email address
    '''
    if re.search('^[a-z0-9]+[\._]*[a-z0-9]+[@]\w+[.]\w{2,3}$', str_inp): # regex needs work
        return True
    return False

#__secret_key = Fernet.generate_key() #this should be the key in production
__secret_key = b'geN2yVD1hAFScLTDmeVuDm69OZ1jWaEST9z9h6Imnkk=' # for temperary porpurse i am assigning a visible string.
__cipher_suite = Fernet(__secret_key)

def encrypt(str_inp):
    '''
    returns the encrypted text of the input string

    Args:
    str_input - the string input which is to be encrypted
    '''
    return __cipher_suite.encrypt(str_inp.encode()).decode()

def decrypt(cipher_data):
    '''
    returns the decrypted text of the input string

    Args:
    cipher_data - the encryption string which need to be decrypted.
    '''
    return __cipher_suite.decrypt(cipher_data.encode()).decode()
