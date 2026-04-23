import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random

# Файл для хранения данных
DATA_FILE = "expenses.json"

class ExpenseManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый менеджер v1.0")
        self.root.geometry("500x600")
        
        self.expenses = self.load_data()
        
        # --- Интерфейс (UI) ---
        self.setup_ui()
        self.update_listbox()

    def setup_ui(self):
        """Создание элементов интерфейса."""
        # Верхняя панель ввода
        input_frame = tk.LabelFrame(self.root, text="Добавить новый расход", padx=10, pady=10)
        input_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(input_frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Сумма:").grid(row=1, column=0, sticky="w")
        self.entry_amount = tk.Entry(input_frame)
        self.entry_amount.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Категория:").grid(row=2, column=0, sticky="w")
        self.combo_category = ttk.Combobox(input_frame, values=["Продукты", "Транспорт", "Развлечения", "Жилье", "Прочее"])
        self.combo_category.current(0)
        self.combo_category.grid(row=2, column=1, padx=5, pady=5)

        self.btn_add = tk.Button(input_frame, text="Добавить", command=self.add_expense, bg="#c8e6c9")
        self.btn_add.grid(row=3, column=0, columnspan=2, pady=10, sticky="we")

        # Список расходов
        list_frame = tk.LabelFrame(self.root, text="История расходов", padx=10, pady=10)
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(list_frame, columns=("Name", "Amount", "Category"), show='headings')
        self.tree.heading("Name", text="Название")
        self.tree.heading("Amount", text="Сумма")
        self.tree.heading("Category", text="Категория")
        self.tree.pack(fill="both", expand=True)

        self.btn_delete = tk.Button(self.root, text="Удалить выбранное", command=self.delete_expense, bg="#ffcdd2")
        self.btn_delete.pack(pady=5)

        # Статистика и советы
        self.label_total = tk.Label(self.root, text="Итого: 0 руб.", font=("Arial", 12, "bold"))
        self.label_total.pack(pady=5)
        self.btn_quote = tk.Button(self.root, text="Получить совет", command=self.show_quote)
        self.btn_quote.pack(pady=5)

    def load_data(self):
        """Загрузка данных из JSON."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self):
        """Сохранение данных в JSON."""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    def add_expense(self):
        """Валидация и добавление расхода."""
        name = self.entry_name.get().strip()
        amount_str = self.entry_amount.get().strip()
        category = self.combo_category.get()

        if not name or not amount_str:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            amount = float(amount_str)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число больше 0")
            return

        new_item = {"name": name, "amount": amount, "category": category}
        self.expenses.append(new_item)
        self.save_data()
        self.update_listbox()
        
        self.entry_name.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)

    def delete_expense(self):
        """Удаление выбранного элемента."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Удаление", "Сначала выберите строку в списке")
            return

        # Получаем индекс элемента
        index = self.tree.index(selected_item)
        del self.expenses[index]
        self.save_data()
        self.update_listbox()

    def update_listbox(self):
        """Обновление таблицы и итоговой суммы."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        total = 0
        for item in self.expenses:
            self.tree.insert("", "end", values=(item["name"], item["amount"], item["category"]))
            total += item["amount"]
        
        self.label_total.config(text=f"Итого: {total:.2f} руб.")

    def show_quote(self):
        """Эмуляция API (или получение случайного совета)."""
        quotes = [
            "Копейка рубль бережёт!",
            "Не покупайте то, что вам не нужно, только потому, что оно дешево.",
            "Планируйте бюджет заранее.",
            "Инвестируйте в знания — они приносят самые высокие проценты."
        ]
        messagebox.showinfo("Совет дня", random.choice(quotes))

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseManager(root)
    root.mainloop()
