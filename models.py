# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin
# from flask_bcrypt import Bcrypt
# from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
# from sqlalchemy.orm.collections import attribute_mapped_collection
# import datetime
# from datetime import date
# from datetime import time
# from datetime import datetime, timedelta
# from wtforms import SelectField, StringField
# from peewee import *

# DATABASE = SQLAlchemy(app)
# bcrypt = Bcrypt()

# class User(UserMixin, Model):
#     __table_args__ = {'extend_existing': True} 
    
#     username = CharField(unique=True)
#     email = CharField(unique=True)
#     password = CharField(max_length=100)
#     name = CharField()
#     height = IntegerField()
#     weight = IntegerField()
#     style = CharField(max_length=20)
#     location = CharField()
#     joined_at = DateTimeField(default=date.today().strftime("%Y-%m-%d"))
#     class Meta:
#         database = DATABASE
#         order_by = ('-timestamp',)
    
#     #  function that creates a new user
#     @classmethod
#     def create_user(cls, username, email , password, name, height, weight, style):
#         try:
#             cls.create(
#                 username = username,
#                 email = email,
#                 password = generate_password_hash(password),
#                 name = name,
#                 height = height,
#                 weight = weight,
#                 style = style
#             )
#         except IntegrityError:
#             raise ValueError("User already exists")


#     def initialize():
#         DATABASE.connect()
#         DATABASE.create_tables([User], safe=True)
#         DATABASE.close()