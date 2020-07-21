from mongoengine import *
from db.db import db


class User(db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField()
    phone_number = db.StringField(required=True)
    encoding = db.ListField()


class Product(db.Document):
    name = db.StringField(required=True)
    price = db.DecimalField(required=True, min_value=0.00, precision=2)


class Order(db.Document):
    user_id = db.StringField(required=True)
    product_ids = db.ListField(required=True)



