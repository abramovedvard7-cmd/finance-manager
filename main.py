import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random

DATA_FILE = "books.json"

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker — Учет прочитанных книг")
        self.root.geometry("600x650")
        
        self.books = self.load_data()
        
        # --- Интерфейс ---
        self.setup_ui()
        self.update_view()

    def setup_ui(self):
        # Фрейм ввода
        input_frame = tk.LabelFrame(self.root, text="Добавить новую книгу", padx=10, pady=10)
        input_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.ent_title = tk.Entry(input_frame)
        self.ent_title.grid(row=0, column=1, padx=5, pady=2, sticky="we")

        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.ent_author = tk.Entry(input_frame)
        self.ent_author.grid(row=1, column=1, padx=5, pady=2, sticky="we")

        tk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky="w")
        self.ent_genre = ttk.Combobox(input_frame, values=["Фантастика", "Детектив", "Роман", "Психология", "Классика", "Другое"])
        self.ent_genre.grid(row=2, column=1, padx=5, pady=2, sticky="we")

        tk.Label(input_frame, text="Страниц:").grid(row=3, column=0, sticky="w")
        self.ent_pages = tk.Entry(input_frame)
        self.ent_pages.grid(row=3, column=1, padx=5, pady=2, sticky="we")

        self.btn_add = tk.Button(input_frame, text="Добавить книгу", command=self.add_book, bg="#bbdefb")
        self.btn_add.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

        # Фрейм фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.filter_genre = ttk.Combobox(filter_frame, values=["Все", "Фантастика", "Детектив", "Роман", "Психология", "Классика", "Другое"])
        self.filter_genre.current(0)
        self.filter_genre.grid(row=0, column=1, padx=5)

        self.btn_filter = tk.Button(filter_frame, text="Применить фильтры", command=self.update_view)
        self.btn_filter.grid(row=0, column=2, padx=5)

        self.check_pages = tk.BooleanVar()
        tk.Checkbutton(filter_frame, text="Более 200 страниц", variable=self.check_pages, command=self.update_view).grid(row=0, column=3)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Стр.")
        self.tree.pack(padx=10, pady=5, fill="both", expand=True)

        # Кнопка удаления и цитата
        btn_del = tk.Button(self.root, text="Удалить выбранную", command=self.delete_book, bg="#ffcdd2")
        btn_del.pack(pady=5)

        self.btn_quote = tk.Button(self.root, text="Случайная цитата", command=self.show_quote)
        self.btn_quote.pack(pady=5)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self):
        t, a, g, p = self.ent_title.get(), self.ent_author.get(), self.ent_genre.get(), self.ent_pages.get()
        
        if not t or not a or not g or not p:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return
        
        try:
            pages = int(p)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        self.books.append({"title": t, "author": a, "genre": g, "pages": pages})
        self.save_data()
        self.update_view()
        self.ent_title.delete(0, tk.END); self.ent_author.delete(0, tk.END); self.ent_pages.delete(0, tk.END)

    def delete_book(self):
        selected = self.tree.selection()
        if not selected: return
        idx = self.tree.index(selected[0])
        # Чтобы правильно удалить при фильтрации, нужно найти книгу по названию или ID
        # Но для простоты удалим из текущего отображения
        book_to_del = self.tree.item(selected[0])['values'][0]
        self.books = [b for b in self.books if b['title'] != book_to_del]
        self.save_data()
        self.update_view()

    def update_view(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        
        f_genre = self.filter_genre.get()
        only_big = self.check_pages.get()

        for b in self.books:
            if f_genre != "Все" and b['genre'] != f_genre: continue
            if only_big and b['pages'] <= 200: continue
            self.tree.insert("", "end", values=(b['title'], b['author'], b['genre'], b['pages']))

    def show_quote(self):
        quotes = ["Книга — лучший подарок.", "Чтение — вот лучшее учение!", "Комната без книг подобна телу без души."]
        messagebox.showinfo("Цитата", random.choice(quotes))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
