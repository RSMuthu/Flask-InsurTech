from flask import make_response, render_template, session, redirect, url_for
from flask_restful import Resource
from extras import decrypt
from database.models import Company
from database.serializer import comp_schema
from cryptography.fernet import InvalidToken
from .security import verify_login

### All resources here will be rendering pages for users

class Form_Entry(Resource):
    def get(self, cipher_id):
        '''
        This is accessed by navigating to the url shared to the company contact person for the form update.

        failure:
                404 (Not Found if company ID not valid)
                405 (Method not allowed if the company form already submitted)
        Success: 200

        Arg:
        cipher_id - the encrypted form of the company ID shared to contact person over email.
        '''
        headers = {'Content-Type': 'text/html'}
        try:
            id_ = decrypt(cipher_id)
            comp = Company.query.filter_by(id=int(id_)).first()
            if comp is None:
                raise InvalidToken
        except InvalidToken:
            return make_response(render_template("error.html", data= {"msg": "PAge Not found", "err": "404"}), 404, headers)
        if comp.is_form_done:
            return make_response(render_template("error.html", data= {"msg": "Company Form update not allowed", "err": "405"}), 405, headers)

        #return resp_dict, 200
        return make_response(render_template("form.html", data=comp_schema.dump(comp)), 200, headers)

class Msg_Board(Resource):
    def get(self, cipher_id):
        '''
        render the Message board template

        failure: 400 (bad request if the resolved company id is invalid)
        success: 200

        Arg:
        cipher_id - the encrypt version of the company id
        '''
        headers = {'Content-Type': 'text/html'}
        try:
            id_ = decrypt(cipher_id)
            comp = Company.query.filter_by(id=int(id_)).first()
            if comp is None:
                raise InvalidToken
        except InvalidToken:
            return make_response(render_template("error.html", data= {"msg": "PAge Not found", "err": "404"}), 404, headers)
        if not comp.is_form_done:
            return make_response(render_template("error.html", data= {"msg": "Company form not filled", "err": "405"}), 405, headers)

        return make_response(render_template("msg_board.html", data= {"c_name": comp.c_name, "product": comp.product, "c_id": comp.id}), 200, headers)

class DashBoard(Resource):
    @verify_login
    def get(self):
        '''
        render the dashboard after authentication

        success: 200
        '''
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("dashboard.html", user=session['usr']), 200, headers)

class Index_Login(Resource):
    def get(self):
        '''
        render the initial page of website

        success: 200
        '''
        if 'usr' in session:
            return redirect(url_for('dashboard'))
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("index.html", token="helloooooo!!!"), 200, headers)
