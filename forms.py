from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextField, TextAreaField, SubmitField, StringField, PasswordField, IntegerField, FileField
from wtforms import SelectField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo, NumberRange)
from flask_login import UserMixin, current_user
from flask_bcrypt import generate_password_hash
import models

def name_exists(form, field):
    if User.select().where(User.username == field.data). exists():
        raise ValidationError("User with this username already exists!")

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("Someone with this email is already in the DB")


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, numbers, and underscores only")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=2),
            EqualTo('Password2', message='Passwords must match')
        ])
    Password2 = PasswordField(
        'Confirm Password',
        validators = [DataRequired()]
    )
    name = StringField(
        'Name',
        validators = [
            DataRequired()
        ])
    height = IntegerField(
        'Height in Inches',
        validators=[
            NumberRange(min= 36, max=99, message='Incorrect input. Height must be greater than 36 inches and less than 99 inches')
        ]
        )
    weight = IntegerField(
        'Weight in Pounds',
        validators = [
            NumberRange(min= None, max=999, message='Please input a weight less than 1000 pounds')
        ]
        )
    style = TextAreaField(
        'Fighting Style',
        validators = [
            DataRequired()
        ])
    picture = FileField(
        'Update Profile Picture', 
        validators = [
            FileAllowed(['jpg', 'png', 'jpeg', 'gif']) 
        ])

    about = TextAreaField(
        'About me...',
        
    )

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired() ])

class FightForm(Form):
    name = TextField("Title", validators = [
            DataRequired()
        ])
    description = TextAreaField("Fight requirements: \n length: \n rules: \n Misc notes:",validators = [
            DataRequired()
        ])
    location = TextField("Venue", validators = [
            DataRequired()
        ])
    submit = SubmitField('Fight!')

class UploadForm(Form):
    picture = FileField('Update Profile Picture', validators = [ FileAllowed(['jpg', 'png', 'jpeg', 'gif']) ])
    Submit = SubmitField('Upload')

class EditFightForm(Form):
    name = TextField("By:")
    title = TextField("Title")
    description = TextAreaField("Content", validators = [
            DataRequired()
        ])
    location = TextField("Venue", validators = [
            DataRequired()
        ])
    submit = SubmitField('Edit Fight request')

class UpdateUserForm(Form):
    username = StringField("Username", validators=[DataRequired(),Length(min=2, max=20), ])
    email = StringField("Email", validators=[DataRequired(),Email(), ])
    name = StringField("Full Name")
    height = IntegerField('Inches')
    weight = IntegerField("lbs")
    style = TextAreaField("Fighting Style")
    about = TextAreaField('Tell us a little about yourself...')
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif']) ])
    submit = SubmitField('Save')

class FollowForm(Form):
    follower_id = IntegerField(validators=[DataRequired()])
    followed_id = IntegerField(validators=[DataRequired()])
    submit =  SubmitField('Challange')

    def name_exists(form, field):
        if User.select().where(User.username == field.data).exists():
            raise ValidationError("User with this username already exists!")

    def email_exists(form, field):
        if User.select().where(User.email == field.data).exists():
            raise ValidationError("Someone with this email is already in the DB")
