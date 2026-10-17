import os
from dotenv import load_dotenv
from mongoengine import connect, Document, StringField, DateField, ReferenceField, ListField, NotUniqueError

load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
if MONGO_URI:
    connect(host=MONGO_URI)
else:
    raise EnvironmentError("MONGO_URI environment variable not set. Cannot connect to MongoDB.")


class Author(Document):
    fullname = StringField(max_length=50, required=True, unique=True)
    born_date = StringField(required=True)
    born_location = StringField(max_length=100, required=True)
    description = StringField(required=True)
    meta = {'collection': 'authors'}


class Quote(Document):
    tags = ListField(StringField(max_length=30), required=True)
    author = ReferenceField('Author', required=True)
    quote = StringField(required=True)
    meta = {'collection': 'quotes'}