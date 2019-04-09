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

# class User(db.Model, UserMixin):
#     __table_args__ = {'extend_existing': True} 
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     height = db.Column(db.Integer, nullable=False)
#     weight = db.Column(db.Integer, nullable=False)
#     style = db.Column(db.String, nullable=False)
#     about = db.Column(db.String(450), unique=True, nullable=False)
    
#     class Meta:
#         database = DATABASE
#         order_by = ('-timestamp',)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}, {self.height}, {self.weight}, {self.style}, {self.about}')"

class Fight(Model):
    name = CharField(max_length=10)
    description = TextField()
    timestamp = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    user = ForeignKeyField(User, backref="fights")

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

class FileContents(Model): 
    __table_args__ = {'extend_existing': True} 
    name = CharField(max_length=300, unique=True)
    # data = db.Column(db.LargeBinary, unique=True)
    user_id = ForeignKeyField(User.id, backref='filecontents')
    user = ForeignKeyField(User, backref="filecontents")



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Fight], safe=True)
    DATABASE.close()