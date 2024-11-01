from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange

class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm_password', message="Passwords should match")])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired()])
    contact_number = StringField("Contact Number", validators=[
        InputRequired(), Length(min=10, message="Contact number must be minimum of 10 digits")])    
    address = StringField("Address", validators=[InputRequired()])
    submit = SubmitField("Register")

class TicketBookingForm(FlaskForm):
    ticket_quantity = IntegerField("Number of Tickets", validators=[InputRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField("Book Now")