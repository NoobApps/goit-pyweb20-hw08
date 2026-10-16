import json
import pika
from faker import Faker
from models import Contact

fake = Faker()


def main(contacts_count=10):
    # 1. Підключення до RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", credentials=pika.PlainCredentials('noob','noob'))
    )
    channel = connection.channel()

    # Оголошуємо чергу (якщо її ще немає)
    queue_name = "email_queue"
    channel.queue_declare(queue=queue_name, durable=True)

    print(f"Генерація та збереження {contacts_count} контактів...")

    for _ in range(contacts_count):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
        ).save()

        message = {"contact_id": str(contact.id)}

        # Публікація повідомлення в чергу
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent  # Збереження повідомлень при перезапуску
            ),
        )

        print(
            f" [x] Створено контакт: {contact.full_name} ({contact.email}) | ID: {contact.id}"
        )

    connection.close()
    print("повідомлення успішно додано до черги!")


if __name__ == "__main__":
    main(contacts_count=10)