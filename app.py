from flask import Flask, jsonify
from flask_restful import Api
import os

from services import initialise_routes, initialise_security
from database import initialise_db, initialise_serializer

app = Flask(__name__, template_folder="templates", static_folder="static")

api = Api(app)        # binding with RESTful aPI

initialise_db(app)     # set DB models ready for use
initialise_serializer(app) # sets the serializer for db query response
initialise_routes(api) # set the endpoints for customer availability
initialise_security(app)


if __name__ == '__main__':
     app.run(port=5002, debug=True)
