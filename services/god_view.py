from flask import make_response
from flask_restful import Resource, reqparse
from database.models import User, Company, Message
from database.serializer import users_schema, comps_schema, msgs_schema

'''
Models peeking can also be made with single get method with dynamic import ...
'''

class Company_view(Resource):
    def get(self):
        '''
        Endpoint to peep into User Table
        '''
        headers = {'Content-Type': 'text/html'}
        comps = Company.query.all()
        return comps_schema.dump(comps), 200

class User_view(Resource):
    def get(self):
        '''
        Endpoint to peep into User Table
        '''
        headers = {'Content-Type': 'text/html'}
        users = User.query.all()
        return users_schema.dump(users), 200

class Message_view(Resource):
    def get(self):
        '''
        Endpoint to peep into Message Table
        '''
        headers = {'Content-Type': 'text/html'}
        msgs = Message.query.all()
        return msgs_scheme.dump(msgs), 200
