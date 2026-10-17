import os
from dotenv import load_dotenv

from mongoengine import connect, Document, EmailField, StringField, BooleanField

load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
if MONGO_URI:
    connect(host=MONGO_URI)
else:
    raise EnvironmentError("MONGO_URI environment variable not set. Cannot connect to MongoDB.")



class Contact(Document):
    full_name = StringField(required=True, max_length=120)
    email = EmailField(required=True, unique=True)
    is_sent = BooleanField(default=False)  # Статус відправки листа
    phone = StringField(max_length=30)  # Додаткове інформаційне поле
    meta = {"collection": "contacts"}
