import datetime
from datetime import date
from datetime import time
from datetime import datetime, timedelta
from wtforms import TextField, TextAreaField, SubmitField, StringField, PasswordField, IntegerField, FileField
from app import db
from wtforms import SelectField
from sqlalchemy.orm import relationship
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('grapplr.db')

class User(UserMixin, Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True} 

    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    name = CharField()
    height = IntegerField()
    weight = IntegerField()
    style = CharField(max_length=20)
    about = CharField(max_length=450)
    image_file = CharField(max_length=20, default='tyler2.jpg')
    # location = CharField()
    joined_at = DateTimeField(default=date.today().strftime("%d/%B/%Y"))
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def follow(self, user):
        if not self.is_following(user):
            self.challanged.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.challanged.remove(user)

    def is_following(self, user):
        return self.challanged.filter(
            challangers.c.challanged_id == user.id).count() > 0


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
    # username = ForeignKeyField(User.username, backref="fights")
    location = TextField()
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)
    
def initialize():
    # db.create_all()
    # models.initialize()
    DATABASE.connect()
    DATABASE.create_tables([User, Fight], safe=True)
    DATABASE.close()