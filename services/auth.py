from flask_restful import Resource, reqparse
from flask import redirect, url_for, make_response, escape, session
from extras import validate_email
from database.models import User, db
from .general_routes import DashBoard
from .security import verify_login
import datetime

class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('passwd', type=str, required=True)

    def post(self):
        '''
        sends post request to register the user for signing up

        failure: send error code - 409 conflict (user already exist), 400 (bad request as the email is not valid)
        success: 201

        Args:
        email - the email address of user
        passwd - the password for login
        '''
        data = Register.parser.parse_args()
        if not validate_email(data['email']):
            return {"msg": "Invalid EMail ID"}, 400
        if User.query.filter_by(email=data['email']).scalar() is None:
            usr = User(email=data['email'], passwd=data["passwd"])
            db.session.add(usr)
            db.session.commit()
            return {'msg': "SignUp Success !!"}, 201
        return {"msg": "User already exists"}, 409

class Login(Resource):
    def post(self):
        '''
        sends post request to login with user credentials

        failure: send error code - 401
        success: 301 redirect to dashboard


        Args:
        email - the email address of user
        passwd - the password for login
        '''
        if 'usr' in session:
            return redirect(url_for('dashboard'))
        data = Register.parser.parse_args()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_pass(escape(data['passwd'])):
            session['usr'] = user.email
            session.permanent = True
            return {"msg": "Login successful"}, 200
        return {'msg': "Invalid username or password"}, 401

class Logout(Resource):
    @verify_login
    def delete(self):
        session.pop("usr", None)
        return {"msg": "Logout Successfully"}, 200
