import json
import os
import random

class QuoteManager:
    """Класс для управления цитатами и историей"""

    def __init__(self, history_file="quotes_history.json"):
        self.history_file = history_file
        
        # Предопределённые цитаты
        self.default_quotes = [
            {"text": "Будь изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "Мотивация"},
            {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "theme": "Жизнь"},
            {"text": "Не трать время на стук в стену, найди дверь.", "author": "Роберт Кийосаки", "theme": "Успех"},
            {"text": "Сложнее всего начать действовать, остальное зависит от упорства.", "author": "Пауло Коэльо", "theme": "Мотивация"},
            {"text": "Будущее зависит от того, что ты делаешь сегодня.", "author": "Махатма Ганди", "theme": "Будущее"},
            {"text": "Единственный способ делать великую работу — любить свою работу.", "author": "Стив Джобс", "theme": "Работа"},
            {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "theme": "Знание"},
            {"text": "Вдохновение приходит только во время работы.", "author": "Габриэль Гарсиа Маркес", "theme": "Творчество"},
            {"text": "Важно не количество знаний, а качество их применения.", "author": "Аристотель", "theme": "Знание"},
            {"text": "Никогда не сдавайся.", "author": "Уинстон Черчилль", "theme": "Мотивация"}
        ]
        
        self.history = self.load_history()
        self.all_quotes = self.load_all_quotes()

    def load_history(self):
        """Загружает историю из JSON"""
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_history(self):
        """Сохраняет историю в JSON"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
            return True
        except IOError:
            return False

    def load_all_quotes(self):
        """Загружает все цитаты (предопределённые + из истории)"""
        # Собираем уникальные цитаты из истории
        history_quotes = []
        seen = set()
        for q in self.history:
            key = (q["text"], q["author"])
            if key not in seen:
                seen.add(key)
                history_quotes.append(q)
        
        # Объединяем с предопределёнными
        return self.default_quotes + history_quotes

    def get_random_quote(self):
        """Возвращает случайную цитату из всех доступных"""
        if not self.all_quotes:
            return None
        quote = random.choice(self.all_quotes)
        
        # Добавляем в историю
        quote_with_time = quote.copy()
        from datetime import datetime
        quote_with_time["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(quote_with_time)
        self.save_history()
        
        return quote

    def get_history(self):
        """Возвращает всю историю"""
        return self.history.copy()

    def clear_history(self):
        """Очищает историю"""
        self.history = []
        self.save_history()
        self.all_quotes = self.load_all_quotes()

    def add_custom_quote(self, text, author, theme):
        """Добавляет пользовательскую цитату"""
        if not text or not text.strip():
            return False, "Текст цитаты не может быть пустым"
        if not author or not author.strip():
            return False, "Автор не может быть пустым"
        if not theme or not theme.strip():
            return False, "Тема не может быть пустой"
        
        new_quote = {
            "text": text.strip(),
            "author": author.strip(),
            "theme": theme.strip()
        }
        self.all_quotes.append(new_quote)
        return True, "Цитата добавлена!"

    def filter_by_author(self, author):
        """Фильтрует историю по автору"""
        if not author:
            return self.history
        author_lower = author.lower().strip()
        return [q for q in self.history if author_lower in q["author"].lower()]

    def filter_by_theme(self, theme):
        """Фильтрует историю по теме"""
        if not theme:
            return self.history
        theme_lower = theme.lower().strip()
        return [q for q in self.history if theme_lower in q["theme"].lower()]

    def get_all_authors(self):
        """Возвращает список уникальных авторов из истории"""
        authors = set()
        for q in self.history:
            if q.get("author"):
                authors.add(q["author"])
        return sorted(list(authors))

    def get_all_themes(self):
        """Возвращает список уникальных тем из истории"""
        themes = set()
        for q in self.history:
            if q.get("theme"):
                themes.add(q["theme"])
        return sorted(list(themes))

    def get_stats(self):
        """Возвращает статистику"""
        return {
            "total_generated": len(self.history),
            "unique_authors": len(self.get_all_authors()),
            "unique_themes": len(self.get_all_themes())
        }