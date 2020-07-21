from flask_mongoengine import MongoEngine
from mongoengine import *

db = MongoEngine()


def initialize_db(app):
    db.init_app(app)


def db_conn():
    connect("reco-app")

