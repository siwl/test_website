from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, \
    TextAreaField, DateField
from wtforms.validators import Required, Optional, Length, Email, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from ..models import User
from wtforms.fields.html5 import DateField


class NewSessionForm(Form):
    year = StringField('Year', validators=[
        Required(), Length(4, 4)])
    room = StringField('Room', validators=[
        Optional(), Length(0, 10)])
    time = StringField('Time', validators=[
        Required(), Length(2, 2)])
    submit = SubmitField('Submit')



class EditProfileForm(Form):
    schoolyear = IntegerField('School Year', validators=[Optional()])
    time = StringField('Time', validators=[Optional(), Length(0, 20)])
    room = StringField('Room', validators=[Optional(), Length(0, 30)])
    duration = IntegerField('Duration', validators=[Optional()])
    submit = SubmitField('Submit')


class AssignTeacherForm(Form):
    teacher = IntegerField('Teacher ID', validators=[Required()])