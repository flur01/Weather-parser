from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,  BooleanField, PasswordField, SelectField, TextAreaField 
from wtforms.validators import DataRequired, Email
from datetime import datetime
from wtforms.fields import *
from wtforms import widgets, Form as _Form
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()


class AddForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname =  StringField("Surname", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(),DataRequired()])
    gender = SelectField('Genfer', choices=[('u', 'unset'),('1', 'male'), ('0', 'female')])
    birthday = DateField('Birthday',format='%Y-%m-%d', default=datetime.now() )
    remember = BooleanField("Remember Me")
    submit = SubmitField()

class AddFeedback(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(),DataRequired()])
    feedback = TextAreaField("Test", validators=[DataRequired()])
    submit = SubmitField()