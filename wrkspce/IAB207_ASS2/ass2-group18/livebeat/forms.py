from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
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
