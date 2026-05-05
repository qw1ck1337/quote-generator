import unittest
import os
import json
from quote_manager import QuoteManager

class TestQuoteGenerator(unittest.TestCase):
    def setUp(self):
        """Создаём тестовый файл перед каждым тестом"""
        self.test_file = "test_history.json"
        self.test_history = [
            {
                "text": "Тестовая цитата",
                "author": "Тест Автор",
                "theme": "Тест",
                "timestamp": "2024-01-01 12:00:00"
            }
        ]
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.test_history, f, ensure_ascii=False)
        self.qm = QuoteManager(self.test_file)

    def tearDown(self):
        """Удаляем тестовый файл после теста"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # Позитивные тесты
    def test_get_random_quote(self):
        quote = self.qm.get_random_quote()
        self.assertIsNotNone(quote)
        self.assertIn("text", quote)
        self.assertIn("author", quote)

    def test_add_valid_quote(self):
        # Сохраняем исходное количество
        initial_count = len(self.qm.all_quotes)
        success, msg = self.qm.add_custom_quote("Новая цитата", "Новый автор", "Новая тема")
        self.assertTrue(success)
        # После добавления должно стать на 1 больше
        self.assertEqual(len(self.qm.all_quotes), initial_count + 1)

    # Негативные тесты
    def test_add_empty_text(self):
        success, msg = self.qm.add_custom_quote("", "Автор", "Тема")
        self.assertFalse(success)
        self.assertIn("пустым", msg)

    def test_add_empty_author(self):
        success, msg = self.qm.add_custom_quote("Текст", "", "Тема")
        self.assertFalse(success)
        self.assertIn("пустым", msg)

    def test_add_empty_theme(self):
        success, msg = self.qm.add_custom_quote("Текст", "Автор", "")
        self.assertFalse(success)
        self.assertIn("пустой", msg)

    # Граничные тесты
    def test_filter_by_author(self):
        filtered = self.qm.filter_by_author("Тест Автор")
        self.assertEqual(len(filtered), 1)

    def test_filter_by_theme(self):
        filtered = self.qm.filter_by_theme("Тест")
        self.assertEqual(len(filtered), 1)

    def test_clear_history(self):
        self.qm.clear_history()
        self.assertEqual(len(self.qm.history), 0)

    def test_stats(self):
        stats = self.qm.get_stats()
        self.assertEqual(stats["total_generated"], 1)
        self.assertEqual(stats["unique_authors"], 1)

    def test_get_all_authors(self):
        authors = self.qm.get_all_authors()
        self.assertEqual(authors, ["Тест Автор"])


if __name__ == "__main__":
    unittest.main()