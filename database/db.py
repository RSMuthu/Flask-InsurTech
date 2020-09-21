from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma = Marshmallow()

def initialise_serializer(app):
    '''
    initialises all the serialisers for the models defined

    app - Flask instance is sent as input for initialing the DB models
    '''
    ma.init_app(app)

db = SQLAlchemy()

def initialise_db (app):
    '''
    initialises all the models defined
    creates the database for the models

    app - Flask instance is sent as input for initialing the DB models
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perilwise.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # this helps to avoid the warning if the SQLAlchemy track modification is enabled (anyways, not needed)

    db.init_app(app)
    with app.app_context():
        db.create_all()
