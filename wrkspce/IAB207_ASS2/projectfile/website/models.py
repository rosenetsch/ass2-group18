from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    Phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
class Event(db.Model):

class Comment(db.Model):

class Order(db.Model):
