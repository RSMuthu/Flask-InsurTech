from flask import request, render_template, make_response
from flask_restful import Resource, reqparse
from database.models import Company, db
from database.serializer import comp_schema, comps_schema
from extras import send_mail, validate_email, encrypt, decrypt
from .security import verify_login
import json

class Company_Create(Resource):

    @verify_login
    def post(self):
        '''
        sends get request to register the company. (only if authenticated)

        failure: 400 (bad request as the email is not valid)
        success: 201

        Args:
        c_name - companu name
        c_addr - company addr
        contact_name - contact person name
        contact_email - contact person mail id
        product - name of the product required
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('c_name', type=str, required=True)
        parser.add_argument('c_addr', type=str, required=True)
        parser.add_argument('product', type=str, required=True)
        parser.add_argument('contact_name', type=str, required=True)
        parser.add_argument('contact_email', type=str, required=True)
        data = parser.parse_args()
        if not validate_email(data["contact_email"]):
            return {"msg": "Invalid EMail id"}, 400
        comp = Company(c_name=data["c_name"], c_addr=data['c_addr'], contact_name=data["contact_name"], \
            contact_email=data['contact_email'], product=data["product"])
        db.session.add(comp)
        db.session.commit()
        #resp_json, resp_code = Trigger_mail.mailer_function(comp.id, comp.contact_name, comp.contact_email) --> if needed to add email feature while creation itself
        #return resp_json, resp_code ## storing and returning it for readability
        return {"msg": "Company Added Successfully"}, 201

    def put(self): # Authorisation not required as the person will be using hyperlink sent to their mail
        '''
        The Company contact person submits the form response through this.
        Ideally call to this will come from the URL we provided the company contact person to update

        failure:
            400 (bad request if company ID not valid)
            405 (Method not allowed if the company form already submitted)
        success: 200

        Args:
        id - the id of the company (string - later converted to int)
        form_data - the form input provided by the company's contact (dict -- from the form submitted)
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True)
        parser.add_argument('form_data', type=dict, required=True)
        data = parser.parse_args()
        comp = Company.query.filter_by(id=int(data['id'])).first()
        if comp is None:
            return {"msg": "Invalid Company ID to update"}, 400 # restricting creation, only update permitted
        if comp.is_form_done:
            return {"msg": "Company Form update not allowed"}, 405
        comp.form_data = json.dumps(data["form_data"])
        comp.is_form_done = True
        db.session.commit()
        return {"msg": "Update successful"}, 200

    @verify_login
    def get(self):
        '''
        get the complete information of a particular company

        failure: 400 (bad request if company ID not valid)
        success: 200

        Args:
        id - the id of the company (string -- later converted to int)
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, required=True)
        data = parser.parse_args()
        comp = Company.query.filter_by(id=int(data['id'])).first()
        if comp is None:
            return {"msg": "Invalid Company ID to update"}, 400
        return comp_schema.dump(comp), 200


class All_Company(Resource):
    @verify_login
    def get(self):
        '''
        gets the complete list of all the companies and its related details...
        '''
        comps = Company.query.all()
        return comps_schema.dump(comps), 200

class Trigger_mail(Resource):
    @verify_login
    def get(self, c_id):
        '''
        trigger remainder email to company contact with the form and message board url

        failure:
                400 (bad request if company ID not valid)
                405 (method not allowed if form has been filled already)
                401 (unauthorised)
        success: 200

        Args:
        id - the id of the company (string -- later converted to int)
        '''
        comp = Company.query.filter_by(id=int(c_id)).first()
        if comp is None:
            return {"msg": "Invalid Company ID"}, 400
        if comp.is_form_done:
            return {"msg": "Company Form alredy submitted. Email notify not allowed anymore"}, 405
        resp, code = Trigger_mail.mailer_function(comp.id, comp.contact_name, comp.contact_email)
        return resp, code ## storing and returning it for readability


    @classmethod
    def mailer_function(cls, id_, name, mail_id):
        cipher_id = encrypt(str(id_))
        url = f"{request.host_url}/company/fill_form/{cipher_id}"
        board_url = f"{request.host_url}/company/msg_board/{cipher_id}"
        msg = f'''Hi {name},
Please fill in the form provided in the following link to complete the Onboarding.
Link - {url}

After form submission, please use the following Link for company message board.
Message Board Link - {board_url}

Regards,
Perilwise - Onboard.
        '''
        try:
            send_mail([mail_id], "Company Onboard - Perilwise", msg)
        except:
            return {"msg": f"Emailer failed. URL to submit form: {url}\nCompany Message Board: {board_url}", "form_url": url, "msg_board": board_url}, 400
        return {"msg": "Email Sent for the company contact"}, 200
