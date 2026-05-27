from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp, Optional
from wtforms.fields import TextAreaField, SelectField, IntegerField, FloatField, DateField, TimeField
from wtforms.validators import NumberRange
from wtforms.validators import ValidationError
from wtforms.fields import (
    SubmitField,
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    IntegerField,
    FloatField,
    DateField,
    TimeField
)

from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    Regexp,
    Optional,
    NumberRange,
    ValidationError
)

from datetime import date

class EventForm(FlaskForm):
    title = StringField("Event Title", validators=[InputRequired()])
    artist = StringField("Artist/Performer", validators=[InputRequired()])
    description = TextAreaField("Event Description", validators=[InputRequired()])

    category = SelectField(
        "Genre",
        choices=[
            ("rock", "Rock"),
            ("pop", "Pop"),
            ("jazz", "Jazz"),
            ("rnb", "RnB"),
            ("soul", "Soul"),
            ("other", "Other"),
        ],
        validators=[InputRequired()],
    )

    ticket_type = SelectField(
        "Ticket Type",
        choices=[
            ("standard", "Standard"),
            ("vip", "VIP"),
            ("premium", "Premium"),
        ],
        validators=[InputRequired()],
    )

    capacity = SelectField(
        "Capacity",
        choices=[
            ("500", "500"),
            ("1000", "1000"),
            ("2000", "2000"),
            ("3000", "3000"),
            ("4000", "4000"),
            ("5000", "5000"),
        ],
        validators=[InputRequired()],
    )
    date = DateField("Event Date", validators=[InputRequired()])
    time = TimeField("Event Start Time", validators=[InputRequired()])
    end_time = TimeField("Event End Time", validators=[Optional()])

    venue_name = StringField("Venue Name", validators=[InputRequired()])
    venue_address = StringField("Venue Address", validators=[InputRequired()])

    standard_price = FloatField(
        "Standard Ticket Price (AUD $)",
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    vip_price = FloatField(
        "VIP Ticket Price (AUD $)",
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    premium_price = FloatField(
        "Premium Ticket Price (AUD $)",
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    image = FileField("Event Image", validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only.')])

    acknowledgement = SelectField(
        "Acknowledgement of Country",
        choices=[
            ("none", "No Acknowledgement of Country"),
            ("generic", "Acknowledgement of Country: generic"),
            ("enhanced", "Acknowledgement of Country: enhanced"),
        ],
        validators=[InputRequired()],
    )

    submit = SubmitField("Save Event")
    def validate_date(self, field):

    if field.data < date.today():

        raise ValidationError(
            "Event date cannot be in the past."
        )

# creates the login information
class LoginForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[
            InputRequired("Enter email address"),
            Email("Please enter a valid email")
        ]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired("Enter your password")]
    )

    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired("Enter first name")])
    last_name = StringField("Surname", validators=[InputRequired("Enter surname")])
    email = StringField(
        "Email Address",
        validators=[InputRequired("Enter email address"), Email("Please enter a valid email")],
    )
    contact_number = StringField("Contact Number", validators=[InputRequired("Enter contact number")])
    street_address = StringField("Street Address", validators=[InputRequired("Enter street address")])
    # password should be equal to the data entered in confirm
    password=PasswordField("Password", validators=[
                  InputRequired(),
                  Length(min=8, message="Password must be at least 8 characters long"),
                  Regexp(r"^(?=.*[A-Z])(?=.*[^A-Za-z0-9]).+$", message="Password must include at least 1 uppercase letter and 1 symbol"),
                  EqualTo('confirm', message="Passwords should match")
                  ])
    confirm = PasswordField("Confirm Password", validators=[InputRequired("Confirm your password")])

    # submit button
    submit = SubmitField("Register")


class BookingForm(FlaskForm):
    ticket_quantity = IntegerField(
        "Ticket quantity",
        validators=[InputRequired(), NumberRange(min=1)],
        default=1,
    )
    submit = SubmitField("Book Now")
