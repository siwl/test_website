from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import Required, Optional, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 50),
                                           Email()])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    address = TextAreaField('Address', validators=[Length(1, 200)])
    nickname = StringField('Nickname', validators=[
        Optional(), Length(0, 15), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Nicknames must have only letters, '
                                          'numbers, dots or underscores')])
    lastname1 = StringField('Last Name (Contact 1)', validators=[
        Required(), Length(1, 30), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Last names must have only letters, '
                                          'numbers, dots or underscores')])
    firstname1 = StringField('First Name (Contact 1)', validators=[
        Required(), Length(1, 30), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'First names must have only letters, '
                                          'numbers, dots or underscores')])
    middlename1 = StringField('Middle Name (Contact 1)', validators=[
        Optional(), Length(0, 30)])
    chname1 = StringField('Chinese Name (Contact 1)', validators=[
        Optional(), Length(0, 30)])
    phone1 = IntegerField('Phone Number (Contact 1)', validators=[
        Required()])
    lastname2 = StringField('Last Name (Contact 2)', validators=[
        Optional(), Length(0, 30)])
    firstname2 = StringField('First Name (Contact 2)', validators=[
        Optional(), Length(0, 30)])
    middlename2 = StringField('Middle Name (Contact 1)', validators=[
        Optional(), Length(0, 30)])
    chname2 = StringField('Chinese Name (Contact 2)', validators=[
        Optional(), Length(0, 30)])
    phone2 = IntegerField('Phone Number (Contact 2)', validators=[
        Optional()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class EditProfileForm(Form):
    last_name1 = StringField('Last Name', validators=[Length(0, 20)])
    first_name1 = StringField('First Name', validators=[Length(0, 20)])
    phone1 = StringField('phone number', validators=[Length(11, 11)])
    submit = SubmitField('Submit')


