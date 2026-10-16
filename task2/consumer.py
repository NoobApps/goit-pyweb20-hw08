import json
import time
import pika
from mongoengine import ValidationError
from models import Contact


def send_email_stub(email: str, name: str) -> bool:
    print(f"Надсилання листа на {email} ({name})...")
    time.sleep(1)  
    print(f"Лист успішно надіслано на {email}")
    return True


def callback(ch, method, properties, body):
    """Обробка повідомлень з черги RabbitMQ."""
    data = json.loads(body.decode("utf-8"))
    contact_id = data.get("contact_id")

    try:
        # Пошук контакту в MongoDB за ObjectId
        contact = Contact.objects(id=contact_id).first()

        if contact:
            if not contact.is_sent:
                send_email_stub(contact.email, contact.full_name)
                contact.update(set__is_sent=True)
                print(
                    f"Статус контакту {contact_id} оновлено на is_sent=True\n"
                )
            else:
                print(
                    f"Лист контакту {contact_id} вже було надіслано раніше.\n"
                )
        else:
            print(f"Контакт з ID {contact_id} не знайдено в БД.\n")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except (ValidationError, Exception) as e:
        print(f" [ERROR] Помилка обробки повідомлення: {e}")
        # Відхилення повідомлення у разі помилки
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost",credentials=pika.PlainCredentials('noob','noob'))
    )
    channel = connection.channel()

    queue_name = "email_queue"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("Чекаю на нові повідомлення з RabbitMQ. Для виходу натисніть CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nStopped")
        channel.stop_consuming()
        connection.close()


if __name__ == "__main__":
    main()