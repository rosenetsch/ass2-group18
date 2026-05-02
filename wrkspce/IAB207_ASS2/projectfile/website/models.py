from . import db
from datetime import datetime
from flask_login import UserMixin
from zoneinfo import ZoneInfo #this is for the brisbane conversion if needed?

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    category = db.Column(db.String(50))
    status = db.Column(db.String(20))  # Open, Sold Out, Cancelled, Inactive
    acknowledgement = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    Phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

#To make local brisbane time (as brisbane operates on AEST)
#if we just want to use UTC time because it is relevant to our application it can be: 
# date = db.Column(db.DateTime, default=datetime.utcnow) instead.
def brisbane_now():
    return datetime.now(ZoneInfo("Australia/Brisbane"))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=brisbane_now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticketquantity = db.Column(db.Integer)
    datebooked = db.Column(db.DateTime(timezone=True), default=brisbane_now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
