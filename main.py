import tkinter as tk
from tkinter import ttk, messagebox
from quote_manager import QuoteManager

class QuoteGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator — Генератор цитат")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")

        # Инициализация менеджера
        self.quote_manager = QuoteManager()

        # Создание интерфейса
        self.create_main_frame()
        self.create_add_quote_frame()
        self.create_filter_frame()
        self.create_history_frame()
        self.create_stats_frame()

        # Обновление данных
        self.refresh_history()
        self.update_stats()
        self.update_filters()

        # Показываем первую случайную цитату
        self.generate_quote()

    def create_main_frame(self):
        """Главная область с генератором цитат"""
        main_frame = tk.Frame(self.root, bg="#2196F3", padx=20, pady=20)
        main_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(main_frame, text="✨ Случайная цитата ✨", 
                 font=("Arial", 16, "bold"), bg="#2196F3", fg="white").pack()

        self.quote_text_label = tk.Label(main_frame, text="", 
                                          font=("Arial", 14, "italic"), 
                                          bg="#2196F3", fg="white", wraplength=700, 
                                          justify="center", pady=20)
        self.quote_text_label.pack()

        self.quote_author_label = tk.Label(main_frame, text="", 
                                            font=("Arial", 12), 
                                            bg="#2196F3", fg="#FFD700", pady=5)
        self.quote_author_label.pack()

        self.quote_theme_label = tk.Label(main_frame, text="", 
                                           font=("Arial", 10), 
                                           bg="#2196F3", fg="#E0E0E0", pady=5)
        self.quote_theme_label.pack()

        generate_btn = tk.Button(main_frame, text="🎲 Сгенерировать новую цитату 🎲",
                                  command=self.generate_quote,
                                  bg="#FF9800", fg="white", 
                                  font=("Arial", 12, "bold"), pady=10)
        generate_btn.pack(pady=10)

    def create_add_quote_frame(self):
        """Форма для добавления новой цитаты"""
        add_frame = tk.LabelFrame(self.root, text="Добавить свою цитату", 
                                    font=("Arial", 10, "bold"),
                                    padx=10, pady=10, bg="#fff")
        add_frame.pack(fill="x", padx=10, pady=5)

        # Текст цитаты
        tk.Label(add_frame, text="Текст цитаты:", bg="#fff").grid(row=0, column=0, sticky="w", pady=2)
        self.quote_text_entry = tk.Text(add_frame, height=3, width=60, wrap="word")
        self.quote_text_entry.grid(row=0, column=1, padx=5, pady=2, columnspan=2)

        # Автор
        tk.Label(add_frame, text="Автор:", bg="#fff").grid(row=1, column=0, sticky="w", pady=2)
        self.author_entry = tk.Entry(add_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Тема
        tk.Label(add_frame, text="Тема:", bg="#fff").grid(row=1, column=2, sticky="w", pady=2)
        self.theme_entry = tk.Entry(add_frame, width=20)
        self.theme_entry.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        # Кнопка добавления
        add_btn = tk.Button(add_frame, text="➕ Добавить цитату", 
                            command=self.add_custom_quote,
                            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)

    def create_filter_frame(self):
        """Блок фильтрации истории"""
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация истории", 
                                      font=("Arial", 10, "bold"),
                                      padx=10, pady=10, bg="#fff")
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по автору
        tk.Label(filter_frame, text="Автор:", bg="#fff").grid(row=0, column=0, sticky="w", padx=5)
        self.author_filter_var = tk.StringVar()
        self.author_combo = ttk.Combobox(filter_frame, textvariable=self.author_filter_var,
                                          width=20, state="readonly")
        self.author_combo.grid(row=0, column=1, padx=5)
        self.author_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_history())

        # Фильтр по теме
        tk.Label(filter_frame, text="Тема:", bg="#fff").grid(row=0, column=2, sticky="w", padx=5)
        self.theme_filter_var = tk.StringVar()
        self.theme_combo = ttk.Combobox(filter_frame, textvariable=self.theme_filter_var,
                                         width=20, state="readonly")
        self.theme_combo.grid(row=0, column=3, padx=5)
        self.theme_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_history())

        # Кнопки управления
        btn_frame = tk.Frame(filter_frame, bg="#fff")
        btn_frame.grid(row=0, column=4, padx=10)

        reset_btn = tk.Button(btn_frame, text="🔄 Сбросить", command=self.reset_filters,
                               bg="#FF9800", fg="white")
        reset_btn.pack(side="left", padx=2)

        clear_btn = tk.Button(btn_frame, text="🗑 Очистить историю", command=self.clear_history,
                               bg="#f44336", fg="white")
        clear_btn.pack(side="left", padx=2)

    def create_history_frame(self):
        """Таблица с историей цитат"""
        history_frame = tk.LabelFrame(self.root, text="История сгенерированных цитат",
                                       font=("Arial", 10, "bold"),
                                       padx=10, pady=10, bg="#fff")
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создание таблицы
        columns = ("Время", "Цитата", "Автор", "Тема")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)

        self.tree.heading("Время", text="Время получения")
        self.tree.heading("Цитата", text="Цитата")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Тема", text="Тема")

        self.tree.column("Время", width=140)
        self.tree.column("Цитата", width=400)
        self.tree.column("Автор", width=150)
        self.tree.column("Тема", width=120)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_stats_frame(self):
        """Блок статистики"""
        self.stats_frame = tk.LabelFrame(self.root, text="Статистика", 
                                          font=("Arial", 10, "bold"),
                                          padx=10, pady=5, bg="#fff")
        self.stats_frame.pack(fill="x", padx=10, pady=5)

        self.stats_label = tk.Label(self.stats_frame, text="", font=("Arial", 10), bg="#fff")
        self.stats_label.pack()

    def generate_quote(self):
        """Генерирует случайную цитату"""
        quote = self.quote_manager.get_random_quote()
        if quote:
            self.quote_text_label.config(text=f"\"{quote['text']}\"")
            self.quote_author_label.config(text=f"— {quote['author']} —")
            self.quote_theme_label.config(text=f"🏷 Тема: {quote['theme']}")
            self.refresh_history()
            self.update_stats()
            self.update_filters()

    def add_custom_quote(self):
        """Добавляет пользовательскую цитату"""
        text = self.quote_text_entry.get("1.0", tk.END).strip()
        author = self.author_entry.get()
        theme = self.theme_entry.get()

        success, msg = self.quote_manager.add_custom_quote(text, author, theme)

        if success:
            messagebox.showinfo("Успех", msg)
            self.quote_text_entry.delete("1.0", tk.END)
            self.author_entry.delete(0, tk.END)
            self.theme_entry.delete(0, tk.END)
            # Обновляем списки фильтров
            self.update_filters()
        else:
            messagebox.showerror("Ошибка", msg)

    def refresh_history(self):
        """Обновляет таблицу истории с учётом фильтров"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        history = self.quote_manager.get_history()

        # Применяем фильтры
        author_filter = self.author_filter_var.get()
        if author_filter and author_filter != "Все авторы":
            history = self.quote_manager.filter_by_author(author_filter)

        theme_filter = self.theme_filter_var.get()
        if theme_filter and theme_filter != "Все темы":
            history = self.quote_manager.filter_by_theme(theme_filter)

        # Заполняем таблицу (от новых к старым)
        for quote in reversed(history):
            self.tree.insert("", "end", values=(
                quote.get("timestamp", "Нет даты"),
                quote["text"],
                quote["author"],
                quote["theme"]
            ))

    def update_stats(self):
        """Обновляет статистику"""
        stats = self.quote_manager.get_stats()
        self.stats_label.config(
            text=f"📊 Всего сгенерировано цитат: {stats['total_generated']} | "
                 f"👤 Уникальных авторов: {stats['unique_authors']} | "
                 f"🏷 Уникальных тем: {stats['unique_themes']}"
        )

    def update_filters(self):
        """Обновляет выпадающие списки фильтров"""
        authors = ["Все авторы"] + self.quote_manager.get_all_authors()
        themes = ["Все темы"] + self.quote_manager.get_all_themes()

        if not self.author_filter_var.get() or self.author_filter_var.get() not in authors:
            self.author_combo['values'] = authors
            self.author_filter_var.set("Все авторы")

        if not self.theme_filter_var.get() or self.theme_filter_var.get() not in themes:
            self.theme_combo['values'] = themes
            self.theme_filter_var.set("Все темы")

    def reset_filters(self):
        """Сбрасывает фильтры"""
        self.author_filter_var.set("Все авторы")
        self.theme_filter_var.set("Все темы")
        self.refresh_history()

    def clear_history(self):
        """Очищает историю (с подтверждением)"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.quote_manager.clear_history()
            self.refresh_history()
            self.update_stats()
            self.update_filters()
            messagebox.showinfo("Очищено", "История успешно очищена!")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGeneratorApp(root)
    root.mainloop()