from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, \
    TextAreaField, DateField, SelectField  
from wtforms.validators import Required, Optional, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from wtforms.fields.html5 import DateField


class NewClassForm(Form):
    name = StringField('Class Name', validators=[
        Required(), Length(1, 30)])
    description = TextAreaField('Description', validators=[
        Required(), Length(1, 100)])
    classtype = SelectField('Type', choices=[
        ('1','Language'), ('2','Bilingual'), ('3','Culture'), ('4','Adult')])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Name', validators=[Length(0, 20)])
    description = TextAreaField('Descrption', validators=[Length(0, 100)])
    classtype = StringField('Class Type', validators=[Length(0, 30)])
    submit = SubmitField('Submit')