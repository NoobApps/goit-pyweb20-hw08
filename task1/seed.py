from models import Author, Quote
import json
from datetime import datetime

def load_authors(file_path="authors.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        authors_data = json.load(file)
        
    for item in authors_data:
        author = Author.objects(fullname=item["fullname"]).first()
        if not author:
            author = Author(
                fullname=item.get("fullname"),
                born_date=datetime.strptime(item.get("born_date"), "%B %d, %Y").date(),
                born_location=item.get("born_location"),
                description=item.get("description")
            )
            author.save()
            print(f"Додано автора: {author.fullname}")
        else:
            print(f"Автор вже існує: {author.fullname}")

def load_quotes(file_path="quotes.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        quotes_data = json.load(file)

    for item in quotes_data:
        author_name = item["author"]
        author = Author.objects(fullname=author_name).first()

        if author:
            # Перевірка на наявність такої ж цитати
            existing_quote = Quote.objects(quote=item["quote"]).first()
            if not existing_quote:
                quote = Quote(
                    tags=item.get("tags", []),
                    author=author,
                    quote=item["quote"]
                )
                quote.save()
                print(f"Додано цитату автора: {author.fullname}")
            else:
                print(f"Цитата вже існує в БД")
        else:
            print(f"Помилка: Автора '{author_name}' не знайдено в базі даних!")

if __name__ == "__main__":
    load_authors()
    load_quotes()
    print("Завантаження даних завершено успішно!")