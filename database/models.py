from datetime import datetime
from extras import md5
from .db import db

class User(db.Model):
    '''
    Model - User
    Table for the User - Holds all the user related information
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    passwd = db.Column(db.String(100), nullable=False)

    def check_pass(self, passwd):
        '''
        to check if input passwd is same as the user's passwd

        Arg:
        passwd - the input password that need to compared with the user's registered password
        '''
        return self.passwd == passwd

    def __repr__(self):
        return f"User {self.id} - {self.email}"

class Company(db.Model):
    '''
    Model Company
    Table for Company - holds all the information related to the companies
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(100), nullable=False)
    c_addr = db.Column(db.Text, nullable=False)
    contact_name = db.Column(db.String(20), nullable=False)
    contact_email = db.Column(db.String(20), nullable=False)
    product = db.Column(db.String(20), nullable=False)
    form_data = db.Column(db.Text, nullable=True)
    is_form_done = db.Column(db.Boolean, nullable=False,default=False)

    def __repr__(self):
        return f'Company {self.id} - {self.c_name}'

class Message(db.Model):
    '''
    Model Message
    Table for Message - holds all the messages from the conversation happening.
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_id = db.Column(db.Integer, nullable=False) # ForeignKey('Company.id') --> yet to implement
    msg = db.Column(db.Text, nullable=False)
    tstamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    by = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'{self.by} [{c_id}]- {self.msg} \n'
