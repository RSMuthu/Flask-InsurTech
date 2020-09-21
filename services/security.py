from flask import jsonify, render_template, make_response, session
from functools import wraps
import datetime

'''
For now, the Flask.seesion is being used for authorization purpose,
To continue much more stateless system, we can use Access tokens to work on (JWT)
Or even a 3rd party server like OAuth or Auth0 & can have SSO or SAML
--- [prefering to go with sessions for now]
'''


def initialise_security (app):
    '''
    initialises all JWT requirements

    app - Flask instance is sent as input for initialing the JWT
    '''

    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
    #app.secret_key = os.random(16) # secret key for encryption
    app.config['SECRET_KEY'] = 'zuwNP63m12iy41247ujawsnkasmc2TpCOGI4nss'

def verify_login(endpoint):
    '''
    decorator to make sure the login is made before accessing certain endpoints
    '''
    @wraps(endpoint)
    def wrapper (*args, **kwargs):
        if 'usr' in session:        ## Not having any role based works... and so made it simple
            x = endpoint (*args, **kwargs)
            return x
        return make_response(render_template("error.html", data={"msg": "Un Authorised Access", "err": 401}), 401)
    return wrapper
