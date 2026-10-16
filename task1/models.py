from mongoengine import connect, Document, StringField, DateField, ReferenceField, ListField, NotUniqueError

connect(host="mongodb+srv://vitalikivaskiv88_db_user:KaQRgV9Sirq5sNc8@cluster0.ua3sivt.mongodb.net/my_quotes_db?retryWrites=true&w=majority")

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