from . import db
from datetime import datetime
from flask_login import UserMixin


def brisbane_now():
    return datetime.now()


# =========================================
# USER MODEL
# =========================================

class User(db.Model, UserMixin):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    address = db.Column(
        db.String(200)
    )

    events = db.relationship(
        "Event",
        backref="creator",
        lazy=True
    )

    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True
    )

    comments = db.relationship(
        "Comment",
        backref="user",
        lazy=True
    )


# =========================================
# EVENT MODEL
# =========================================

class Event(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    artist = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Open"
    )

    capacity = db.Column(
        db.Integer,
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        nullable=False
    )

    # START TIME

    time = db.Column(
        db.Time,
        nullable=False
    )

    # END TIME

    end_time = db.Column(
        db.Time,
        nullable=True
    )

    venue_name = db.Column(
        db.String(120),
        nullable=False
    )

    venue_address = db.Column(
        db.String(200),
        nullable=False
    )

    # STANDARD PRICE

    standard_price = db.Column(
        db.Float,
        nullable=False
    )

    # VIP PRICE

    vip_price = db.Column(
        db.Float,
        nullable=False
    )

    # PREMIUM PRICE

    premium_price = db.Column(
        db.Float,
        nullable=False
    )

    ticket_type = db.Column(
        db.String(50),
        nullable=True,
        default="standard"
    )

    acknowledgement = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(200),
        default="concert1.jpg"
    )

    created_at = db.Column(
        db.DateTime,
        default=brisbane_now
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    bookings = db.relationship(
        "Booking",
        backref="event",
        lazy=True
    )

    comments = db.relationship(
        "Comment",
        backref="event",
        lazy=True
    )


# =========================================
# COMMENT MODEL
# =========================================

class Comment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    date = db.Column(
        db.DateTime,
        default=brisbane_now
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("event.id")
    )


# =========================================
# BOOKING MODEL
# =========================================

class Booking(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    ticket_quantity = db.Column(
        db.Integer,
        nullable=False
    )

    ticket_price = db.Column(
        db.Float,
        nullable=False
    )

    ticket_type = db.Column(
        db.String(50),
        nullable=False,
        default="standard"
    )

    date_booked = db.Column(
        db.DateTime,
        default=brisbane_now
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("event.id")
    )
