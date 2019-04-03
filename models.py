import datetime
from datetime import date
from datetime import time
from datetime import datetime, timedelta
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
    # location = CharField()
    joined_at = DateTimeField(default=date.today().strftime("%Y-%m-%d"))
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)
    
    #  function that creates a new user
    @classmethod
    def create_user(cls, username, email , password, name, height, weight, style):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                name = name,
                height = height,
                weight = weight,
                style = style
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

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Fight], safe=True)
    DATABASE.close()