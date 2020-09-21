from flask_restful import Resource, reqparse
from database.models import Message, Company, db
from database.serializer import msgs_schema

## Better option is to implement this with Kafka or other communication/data passing mechanisms
class Text_Msg(Resource):

    def post(self, c_id):
        '''
        save the message in to the dB

        failure: 400 (bad request if the c_id is not valid)
        success: 200

        Arg:
        c_id - the company id to submit the message to
        msg - the msg string to submit
        name - the name of the person who submitted the message.
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('msg', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        data = parser.parse_args()
        if Company.query.filter_by(id=int(c_id)).first() is None: # best is to use first_or_404() but as i am not going with exception, so handling this way.
            return {"msg", "Invalid Company ID"}, 400
        msg = Message(c_id=int(c_id), by=data["name"], msg=data['msg'])
        db.session.add(msg)
        db.session.commit()
        return {"msg": "Message added to board."}, 200

    def get(self, c_id):
        '''
        get all the messages associated with a company.

        failure: 400 (Bad request if the c_id not valid)
        success: 200

        Arg:
        c_id - company ID for fetching the msg associated to the Company
        '''
        if Company.query.filter_by(id=int(c_id)).first() is None:
            return {"msg": "invalid Company Id"}, 400
        messages = Message.query.filter_by(c_id=int(c_id)).order_by(Message.tstamp.desc()).all()
        return msgs_schema.dump(messages), 200
