from flask_wtf import FlaskForm
from flask_wtf.file import (
    FileField,
    FileAllowed
)

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


# =========================================
# EVENT FORM
# =========================================

class EventForm(FlaskForm):

    title = StringField(

        "Event Title",

        validators=[
            InputRequired()
        ]
    )

    artist = StringField(

        "Artist/Performer",

        validators=[
            InputRequired()
        ]
    )

    description = TextAreaField(

        "Event Description",

        validators=[
            InputRequired()
        ]
    )

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

        validators=[
            InputRequired()
        ],
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

        validators=[
            InputRequired()
        ],
    )

    date = DateField(

        "Event Date",

        validators=[
            InputRequired()
        ]
    )

    # START TIME

    time = TimeField(

        "Event Start Time",

        validators=[
            InputRequired()
        ]
    )

    # END TIME

    end_time = TimeField(

        "Event End Time"
    )

    venue_name = StringField(

        "Venue Name",

        validators=[
            InputRequired()
        ]
    )

    venue_address = StringField(

        "Venue Address",

        validators=[
            InputRequired()
        ]
    )

    # STANDARD PRICE

    standard_price = FloatField(

        "Standard Ticket Price (AUD $)",

        validators=[

            InputRequired(),

            NumberRange(min=0)
        ]
    )

    # VIP PRICE

    vip_price = FloatField(

        "VIP Ticket Price (AUD $)",

        validators=[

            InputRequired(),

            NumberRange(min=0)
        ]
    )

    # PREMIUM PRICE

    premium_price = FloatField(

        "Premium Ticket Price (AUD $)",

        validators=[

            InputRequired(),

            NumberRange(min=0)
        ]
    )

    # IMAGE

    image = FileField(

        "Event Image",

        validators=[

            Optional(),

            FileAllowed(
                ["jpg", "jpeg", "png", "gif"],
                "Images only."
            )
        ]
    )

    acknowledgement = SelectField(

        "Acknowledgement of Country",

        choices=[

            ("none", "No Acknowledgement of Country"),

            ("generic", "Generic"),

            ("enhanced", "Enhanced"),
        ],

        validators=[
            InputRequired()
        ],
    )

    submit = SubmitField(
        "Save Event"
    )

    # DATE VALIDATION

    def validate_date(self, field):

        if field.data < date.today():

            raise ValidationError(
                "Event date cannot be in the past."
            )


# =========================================
# LOGIN FORM
# =========================================

class LoginForm(FlaskForm):

    email = StringField(

        "Email Address",

        validators=[

            InputRequired(
                "Enter email address"
            ),

            Email(
                "Please enter a valid email"
            )
        ]
    )

    password = PasswordField(

        "Password",

        validators=[

            InputRequired(
                "Enter your password"
            )
        ]
    )

    submit = SubmitField(
        "Login"
    )


# =========================================
# REGISTER FORM
# =========================================

class RegisterForm(FlaskForm):

    first_name = StringField(

        "First Name",

        validators=[

            InputRequired(
                "Enter first name"
            )
        ]
    )

    last_name = StringField(

        "Surname",

        validators=[

            InputRequired(
                "Enter surname"
            )
        ]
    )

    email = StringField(

        "Email Address",

        validators=[

            InputRequired(
                "Enter email address"
            ),

            Email(
                "Please enter a valid email"
            ),
        ],
    )

    contact_number = StringField(

        "Contact Number",

        validators=[

            InputRequired(
                "Enter contact number"
            )
        ]
    )

    street_address = StringField(

        "Street Address",

        validators=[

            InputRequired(
                "Enter street address"
            )
        ]
    )

    password = PasswordField(

        "Password",

        validators=[

            InputRequired(),

            Length(
                min=8,
                message="Password must be at least 8 characters long"
            ),

            Regexp(
                r"^(?=.*[A-Z])(?=.*[^A-Za-z0-9]).+$",
                message="Password must include at least 1 uppercase letter and 1 symbol"
            ),

            EqualTo(
                'confirm',
                message="Passwords should match"
            )
        ]
    )

    confirm = PasswordField(

        "Confirm Password",

        validators=[

            InputRequired(
                "Confirm your password"
            )
        ]
    )

    submit = SubmitField(
        "Register"
    )


# =========================================
# BOOKING FORM
# =========================================

class BookingForm(FlaskForm):

    ticket_quantity = IntegerField(

        "Ticket Quantity",

        validators=[

            InputRequired(),

            NumberRange(min=1)
        ],

        default=1,
    )

    submit = SubmitField(
        "Book Now"
    )
