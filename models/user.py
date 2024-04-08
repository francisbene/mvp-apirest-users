from peewee import *

db = SqliteDatabase('users.db')

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)

    class Meta:
        database = db

db.connect()
db.create_tables([User])