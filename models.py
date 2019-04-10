import datetime
from datetime import date
from datetime import time
from datetime import datetime, timedelta
from wtforms import TextField, TextAreaField, SubmitField, StringField, PasswordField, IntegerField, FileField
from app import db
from wtforms import SelectField


#import everything from peewee because we might need it 
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('grapplr.db')



class User(UserMixin, Model):
    __table_args__ = {'extend_existing': True} 
    
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    name = CharField()
    height = IntegerField()
    weight = IntegerField()
    style = CharField(max_length=20)
    about = CharField(max_length=450)
    image_file = CharField(default='tyler2.jpg')
    # location = CharField()
    joined_at = DateTimeField(default=date.today().strftime("%d/%B/%Y"))
    # challanged = db.relationship('User', secondary=user_matches, primaryjoin=(user_matches.c.user_id_1 == id), secondaryjoin=(user_matches.c.user_id_2 == id), backref=db.backref('user_matches', lazy='dynamic'), lazy='dynamic')
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)
    
    #  function that creates a new user
    @classmethod
    def create_user(cls, username, email , password, name, height, weight, style, about, image_file):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                name = name,
                height = height,
                weight = weight,
                style = style,
                about = about,
                image_file = image_file
            )
        except IntegrityError:
            raise ValueError("User already exists")


class Fight(Model):
    name = CharField(max_length=10)
    description = TextField()
    timestamp = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    user = ForeignKeyField(User, backref="fights")

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

# class FileContents(Model): 
#     __table_args__ = {'extend_existing': True} 
#     name = CharField(max_length=300, unique=True)
#     # data = db.Column(db.LargeBinary, unique=True)
#     user_id = ForeignKeyField(User.id, backref='filecontents')
#     user = ForeignKeyField(User, backref="filecontents")

# class User_Matches(Model):
#     __table_args__ = {'extend_existing': True}
#     user_id_1 = ForeignKeyField(User.id, backref='usermatches')
#     user_id_2 = ForeignKeyField(User.id, backref='usermatches')
#     match_date = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    

#     class Meta:
#         database = DATABASE
#         order_by = ('-timestamp',)

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Fight], safe=True)
    DATABASE.close()