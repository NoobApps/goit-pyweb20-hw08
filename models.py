import mongoengine as me

# Підключення до бази даних MongoDB (локальна база 'email_service')
me.connect(host="mongodb+srv://vitalikivaskiv88_db_user:KaQRgV9Sirq5sNc8@cluster0.ua3sivt.mongodb.net/emails_db?retryWrites=true&w=majority")



class Contact(me.Document):
    full_name = me.StringField(required=True, max_length=120)
    email = me.EmailField(required=True, unique=True)
    is_sent = me.BooleanField(default=False)  # Статус відправки листа
    phone = me.StringField(max_length=30)  # Додаткове інформаційне поле
    meta = {"collection": "contacts"}
