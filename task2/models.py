from mongoengine import connect, Document, EmailField, StringField, BooleanField

# Підключення до бази даних MongoDB (локальна база 'email_service')
connect(host="mongodb+srv://vitalikivaskiv88_db_user:KaQRgV9Sirq5sNc8@cluster0.ua3sivt.mongodb.net/emails_db?retryWrites=true&w=majority")



class Contact(Document):
    full_name = StringField(required=True, max_length=120)
    email = EmailField(required=True, unique=True)
    is_sent = BooleanField(default=False)  # Статус відправки листа
    phone = StringField(max_length=30)  # Додаткове інформаційне поле
    meta = {"collection": "contacts"}
