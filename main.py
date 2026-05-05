import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "data/trainings.json"

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.create_widgets()
        self.load_data()
        self.update_table()

    def create_widgets(self):
        # --- Поля ввода ---
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill='x')

        ttk.Label(frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky='w')
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1, sticky='ew', padx=5)

        ttk.Label(frame, text="Тип тренировки:").grid(row=1, column=0, sticky='w')
        self.type_var = tk.StringVar()
        self.type_entry = ttk.Combobox(frame, textvariable=self.type_var,
                                       values=["Кардио", "Сила", "Растяжка", "Йога"])
        self.type_entry.grid(row=1, column=1, sticky='ew', padx=5)

        ttk.Label(frame, text="Длительность (мин):").grid(row=2, column=0, sticky='w')
        self.duration_entry = ttk.Entry(frame)
        self.duration_entry.grid(row=2, column=1, sticky='ew', padx=5)

        # --- Кнопки ---
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Button(btn_frame, text="Добавить тренировку", command=self.add_training).pack(side='left')

        # --- Фильтрация ---
        filter_frame = ttk.Frame(self.root, padding=10)
        filter_frame.pack(fill='x')

        ttk.Label(filter_frame, text="Фильтр по типу:").pack(side='left')
        self.filter_type = tk.StringVar()
        ttk.Combobox(filter_frame, textvariable=self.filter_type,
                     values=["Все", "Кардио", "Сила", "Растяжка", "Йога"],
                     state="readonly").pack(side='left', padx=5)

        ttk.Label(filter_frame, text="Фильтр по дате:").pack(side='left')
        self.filter_date = ttk.Entry(filter_frame)
        self.filter_date.pack(side='left', padx=5)

        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).pack(side='left')

        # --- Таблица ---
        self.tree = ttk.Treeview(self.root, columns=("date", "type", "duration"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("duration", text="Длительность (мин)")
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    # --- Логика ---
    def add_training(self):
        date = self.date_entry.get().strip()
        tr_type = self.type_var.get().strip()
        duration = self.duration_entry.get().strip()

        # Валидация даты
        try:
            datetime.strptime(date, "%d.%m.%Y")
            if not date:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите дату в формате ДД.ММ.ГГГГ")
            return

        # Валидация типа
        if not tr_type:
            messagebox.showerror("Ошибка", "Выберите тип тренировки")
            return

        # Валидация длительности
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        self.trainings.append({"date": date, "type": tr_type, "duration": duration})
        self.save_data()
        self.update_table()

    def update_table(self, filtered_trainings=None):
        for i in self.tree.get_children():
            self.tree.delete(i)

        data = filtered_trainings if filtered_trainings else self.trainings
        for tr in data:
            self.tree.insert("", "end", values=(tr["date"], tr["type"], tr["duration"]))

    def apply_filter(self):
        f_type = self.filter_type.get()
        f_date = self.filter_date.get().strip()

        filtered = self.trainings

        if f_type != "Все":
            filtered = [tr for tr in filtered if tr["type"] == f_type]

        if f_date:
            try:
                datetime.strptime(f_date, "%d.%m.%Y")
                filtered = [tr for tr in filtered if tr["date"] == f_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Дата фильтра в неверном формате")
                return

        self.update_table(filtered)

    # --- Работа с JSON ---
    def save_data(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.trainings = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
