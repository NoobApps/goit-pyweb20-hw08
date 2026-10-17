from models import Author, Quote


def search_by_author(name: str):
    """Пошук цитат за ім'ям автора (без урахування регістру)."""
    author = Author.objects(fullname__iexact=name.strip()).first()
    if not author:
        print(f"Автора '{name}' не знайдено.")
        return

    quotes = Quote.objects(author=author)
    if not quotes:
        print(f"Цитат для автора '{author.fullname}' не знайдено.")
        return

    print(f"цитати автора {author.fullname}:")
    for q in quotes:
        # Безпечний вивід у форматі UTF-8
        print(f"- {q.quote}")


def search_by_tag(tag: str):
    """Пошук цитат за одним тегом."""
    quotes = Quote.objects(tags__iexact=tag.strip())
    if not quotes:
        print(f"Цитат з тегом '{tag}' не знайдено.")
        return

    print(f"\nцитaти за тегом '{tag}':")
    for q in quotes:
        print(f"- [{q.author.fullname}]: {q.quote}")


def search_by_tags(tags_str: str):
    """Пошук цитат за списком тегів (через кому, умова OR)."""
    # Розбиваємо рядок на список тегів та видаляємо зайві пробіли
    tags_list = [t.strip() for t in tags_str.split(",") if t.strip()]
    
    # Використовуємо оператор __in для пошуку будь-якого з тегів
    quotes = Quote.objects(tags__in=tags_list)
    if not quotes:
        print(f"Цитат з тегами '{tags_str}' не знайдено.")
        return

    print(f"\nцитaти за тегами [{', '.join(tags_list)}]:")
    for q in quotes:
        print(f"- [{q.author.fullname}]: {q.quote}")


# 4. Основний цикл обробки команд
def main():
    print("Введіть команду в форматі 'команда: значення' ( 'exit' для виходу):")

    while True:
        try:
            user_input = input("\Введіть команду: ").strip()

            if not user_input:
                continue

            # Завершення роботи
            if user_input.lower() == "exit":
                print("Завершення роботи")
                break

            # Розбір команди та значення
            if ":" not in user_input:
                print("Помилка: Невірний формат. Використовуйте 'команда:значення'")
                continue

            command, value = user_input.split(":", 1)
            command = command.strip().lower()
            value = value.strip()

            if command == "name":
                search_by_author(value)
            elif command == "tag":
                search_by_tag(value)
            elif command == "tags":
                search_by_tags(value)
            else:
                print(f"Невідома команда '{command}'. Доступні: name, tag, tags, exit")

        except KeyboardInterrupt:
            print("\Припинено користувачем.")
            break
        except Exception as e:
            print(f"Виникла помилка: {e}")


if __name__ == "__main__":
    main()