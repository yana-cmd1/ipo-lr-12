import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

# ========== МОДЕЛИ ДАННЫХ ==========

class TransportType(Enum):
    TRUCK = "Грузовик"
    TRAIN = "Поезд"

@dataclass
class Client:
    name: str
    cargo_weight: float
    is_vip: bool = False
    
    def to_dict(self):
        return {
            "name": self.name,
            "cargo_weight": self.cargo_weight,
            "is_vip": self.is_vip
        }

@dataclass
class Transport:
    transport_id: int
    transport_type: TransportType
    capacity: float
    current_load: float = 0.0
    
    def to_dict(self):
        return {
            "id": self.transport_id,
            "type": self.transport_type.value,
            "capacity": self.capacity,
            "current_load": self.current_load
        }

# ========== ОСНОВНОЙ КЛАСС ПРИЛОЖЕНИЯ ==========

class CargoDistributionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Распределение грузов - Лабораторная работа")
        self.root.geometry("1200x700")
        
        # Инициализация данных
        self.clients: List[Client] = []
        self.transports: List[Transport] = []
        self.next_transport_id = 1
        
        # Создание интерфейса
        self.setup_menu()
        self.setup_widgets()
        self.setup_statusbar()
        
    # ========== НАСТРОЙКА МЕНЮ ==========
    
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Экспорт результата", 
                            command=self.export_results,
                            accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        
        # Привязка горячих клавиш
        self.root.bind('<Control-e>', lambda e: self.export_results())
        
    # ========== НАСТРОЙКА ОСНОВНЫХ ВИДЖЕТОВ ==========
    
    def setup_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Конфигурация веса строк и столбцов
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Панель управления
        control_frame = ttk.LabelFrame(main_frame, text="Панель управления", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Кнопки управления
        buttons = [
            ("Добавить клиента", self.add_client),
            ("Добавить транспорт", self.add_transport),
            ("Удалить выбранного клиента", self.delete_client),
            ("Удалить выбранный транспорт", self.delete_transport),
            ("Распределить грузы", self.distribute_cargo),
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(control_frame, text=text, command=command)
            btn.grid(row=0, column=i, padx=5)
            # Добавляем всплывающие подсказки
            if "клиента" in text.lower():
                self.create_tooltip(btn, "Добавление нового клиента в систему")
            elif "транспорт" in text.lower():
                self.create_tooltip(btn, "Добавление нового транспортного средства")
            elif "удалить" in text.lower():
                self.create_tooltip(btn, "Удалить выбранный элемент из таблицы")
            elif "распределить" in text.lower():
                self.create_tooltip(btn, "Выполнить оптимизацию распределения грузов")
        
        # Фрейм для таблиц
        tables_frame = ttk.Frame(main_frame)
        tables_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        tables_frame.columnconfigure(0, weight=1)
        tables_frame.columnconfigure(1, weight=1)
        tables_frame.rowconfigure(0, weight=1)
        
        # Таблица клиентов
        self.setup_clients_table(tables_frame)
        
        # Таблица транспорта
        self.setup_transports_table(tables_frame)
        
    def setup_clients_table(self, parent):
        frame = ttk.LabelFrame(parent, text="Клиенты", padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # Создание Treeview
        columns = ("name", "weight", "vip")
        self.clients_tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        
        # Настройка колонок
        self.clients_tree.heading("name", text="Имя клиента")
        self.clients_tree.heading("weight", text="Вес груза (кг)")
        self.clients_tree.heading("vip", text="VIP статус")
        
        self.clients_tree.column("name", width=200)
        self.clients_tree.column("weight", width=100, anchor=tk.CENTER)
        self.clients_tree.column("vip", width=80, anchor=tk.CENTER)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.clients_tree.yview)
        self.clients_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение
        self.clients_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Привязка двойного клика для редактирования
        self.clients_tree.bind("<Double-1>", lambda e: self.edit_client())
        
    def setup_transports_table(self, parent):
        frame = ttk.LabelFrame(parent, text="Транспортные средства", padding="10")
        frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # Создание Treeview
        columns = ("id", "type", "capacity", "load")
        self.transports_tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        
        # Настройка колонок
        self.transports_tree.heading("id", text="ID")
        self.transports_tree.heading("type", text="Тип транспорта")
        self.transports_tree.heading("capacity", text="Грузоподъемность")
        self.transports_tree.heading("load", text="Текущая загрузка")
        
        self.transports_tree.column("id", width=50, anchor=tk.CENTER)
        self.transports_tree.column("type", width=100)
        self.transports_tree.column("capacity", width=120, anchor=tk.CENTER)
        self.transports_tree.column("load", width=120, anchor=tk.CENTER)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.transports_tree.yview)
        self.transports_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение
        self.transports_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Привязка двойного клика для редактирования
        self.transports_tree.bind("<Double-1>", lambda e: self.edit_transport())
        
    # ========== НАСТРОЙКА СТРОКИ СОСТОЯНИЯ ==========
    
    def setup_statusbar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Готово")
        statusbar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        statusbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def update_status(self, message):
        self.status_var.set(message)
        self.root.after(3000, lambda: self.status_var.set("Готово") if self.status_var.get() == message else None)
        
    # ========== ОКНА РЕДАКТИРОВАНИЯ ==========
    
    def add_client(self):
        self.open_client_window()
        
    def edit_client(self):
        selection = self.clients_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите клиента для редактирования")
            return
            
        item = self.clients_tree.item(selection[0])
        client_index = self.clients_tree.index(selection[0])
        self.open_client_window(self.clients[client_index], client_index)
        
    def open_client_window(self, client=None, index=None):
        window = tk.Toplevel(self.root)
        window.title("Добавление клиента" if client is None else "Редактирование клиента")
        window.geometry("400x250")
        window.transient(self.root)
        window.grab_set()
        
        # Переменные
        name_var = tk.StringVar(value=client.name if client else "")
        weight_var = tk.DoubleVar(value=client.cargo_weight if client else 0.0)
        vip_var = tk.BooleanVar(value=client.is_vip if client else False)
        
        # Валидация
        def validate_name(char):
            return char.isalpha() or char in " -"
        
        def validate_weight(char):
            return char.isdigit() or char == "."
        
        # Виджеты
        ttk.Label(window, text="Имя клиента:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_entry = ttk.Entry(window, textvariable=name_var, validate="key")
        name_entry.configure(validatecommand=(window.register(lambda char: validate_name(char)), '%S'))
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.create_tooltip(name_entry, "Только буквы, минимум 2 символа")
        
        ttk.Label(window, text="Вес груза (кг):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        weight_entry = ttk.Entry(window, textvariable=weight_var, validate="key")
        weight_entry.configure(validatecommand=(window.register(lambda char: validate_weight(char)), '%S'))
        weight_entry.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.create_tooltip(weight_entry, "Положительное число, не более 10000 кг")
        
        vip_check = ttk.Checkbutton(window, text="VIP статус", variable=vip_var)
        vip_check.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
        
        # Кнопки
        button_frame = ttk.Frame(window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def save():
            name = name_var.get().strip()
            weight = weight_var.get()
            
            # Валидация
            errors = []
            if len(name) < 2:
                errors.append("Имя должно содержать минимум 2 символа")
            if not name.replace(" ", "").replace("-", "").isalpha():
                errors.append("Имя должно содержать только буквы")
            if weight <= 0:
                errors.append("Вес груза должен быть положительным числом")
            if weight > 10000:
                errors.append("Вес груза не может превышать 10000 кг")
            
            if errors:
                messagebox.showerror("Ошибка валидации", "\n".join(errors))
                return
            
            if client is None:
                # Добавление
                new_client = Client(name, weight, vip_var.get())
                self.clients.append(new_client)
                self.update_status("Клиент добавлен")
                messagebox.showinfo("Успех", "Клиент успешно добавлен")
            else:
                # Редактирование
                self.clients[index] = Client(name, weight, vip_var.get())
                self.update_status("Клиент обновлен")
                messagebox.showinfo("Успех", "Данные клиента обновлены")
            
            self.refresh_tables()
            window.destroy()
        
        ttk.Button(button_frame, text="Сохранить", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Привязка клавиш
        window.bind('<Return>', lambda e: save())
        window.bind('<Escape>', lambda e: window.destroy())
        
        # Фокус
        name_entry.focus_set()
        window.columnconfigure(1, weight=1)
        
    def add_transport(self):
        self.open_transport_window()
        
    def edit_transport(self):
        selection = self.transports_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите транспорт для редактирования")
            return
            
        item = self.transports_tree.item(selection[0])
        transport_index = self.transports_tree.index(selection[0])
        self.open_transport_window(self.transports[transport_index], transport_index)
        
    def open_transport_window(self, transport=None, index=None):
        window = tk.Toplevel(self.root)
        window.title("Добавление транспорта" if transport is None else "Редактирование транспорта")
        window.geometry("400x300")
        window.transient(self.root)
        window.grab_set()
        
        # Переменные
        type_var = tk.StringVar(value=transport.transport_type.value if transport else TransportType.TRUCK.value)
        capacity_var = tk.DoubleVar(value=transport.capacity if transport else 1000.0)
        
        # Валидация
        def validate_capacity(char):
            return char.isdigit() or char == "."
        
        # Виджеты
        ttk.Label(window, text="Тип транспорта:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        type_combo = ttk.Combobox(window, textvariable=type_var, 
                                 values=[t.value for t in TransportType], state="readonly")
        type_combo.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(window, text="Грузоподъемность (кг):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        capacity_entry = ttk.Entry(window, textvariable=capacity_var, validate="key")
        capacity_entry.configure(validatecommand=(window.register(lambda char: validate_capacity(char)), '%S'))
        capacity_entry.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.create_tooltip(capacity_entry, "Положительное число, максимальная грузоподъемность")
        
        # Кнопки
        button_frame = ttk.Frame(window)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def save():
            try:
                capacity = capacity_var.get()
                
                # Валидация
                if capacity <= 0:
                    messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительным числом")
                    return
                
                transport_type = TransportType(type_var.get())
                
                if transport is None:
                    # Добавление
                    new_transport = Transport(self.next_transport_id, transport_type, capacity)
                    self.next_transport_id += 1
                    self.transports.append(new_transport)
                    self.update_status("Транспорт добавлен")
                    messagebox.showinfo("Успех", "Транспортное средство успешно добавлено")
                else:
                    # Редактирование
                    self.transports[index] = Transport(
                        transport.transport_id, transport_type, capacity, transport.current_load
                    )
                    self.update_status("Транспорт обновлен")
                    messagebox.showinfo("Успех", "Данные транспорта обновлены")
                
                self.refresh_tables()
                window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
        
        ttk.Button(button_frame, text="Сохранить", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Привязка клавиш
        window.bind('<Return>', lambda e: save())
        window.bind('<Escape>', lambda e: window.destroy())
        
        # Фокус
        type_combo.focus_set()
        window.columnconfigure(1, weight=1)
        
    # ========== ОПЕРАЦИИ С ДАННЫМИ ==========
    
    def delete_client(self):
        selection = self.clients_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите клиента для удаления")
            return
            
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранного клиента?"):
            for item in selection:
                index = self.clients_tree.index(item)
                del self.clients[index]
            
            self.refresh_tables()
            self.update_status("Клиент удален")
            
    def delete_transport(self):
        selection = self.transports_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите транспорт для удаления")
            return
            
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранный транспорт?"):
            for item in selection:
                index = self.transports_tree.index(item)
                del self.transports[index]
            
            self.refresh_tables()
            self.update_status("Транспорт удален")
            
    def distribute_cargo(self):
        if not self.clients:
            messagebox.showwarning("Предупреждение", "Добавьте клиентов для распределения")
            return
            
        if not self.transports:
            messagebox.showwarning("Предупреждение", "Добавьте транспортные средства")
            return
        
        # Сброс текущей загрузки
        for transport in self.transports:
            transport.current_load = 0
        
        # Простой алгоритм распределения (VIP клиенты имеют приоритет)
        vip_clients = [c for c in self.clients if c.is_vip]
        regular_clients = [c for c in self.clients if not c.is_vip]
        
        # Распределение VIP клиентов
        for client in vip_clients:
            for transport in self.transports:
                if transport.current_load + client.cargo_weight <= transport.capacity:
                    transport.current_load += client.cargo_weight
                    break
        
        # Распределение обычных клиентов
        for client in regular_clients:
            distributed = False
            for transport in self.transports:
                if transport.current_load + client.cargo_weight <= transport.capacity:
                    transport.current_load += client.cargo_weight
                    distributed = True
                    break
            
            if not distributed:
                messagebox.showwarning("Внимание", 
                                    f"Груз клиента {client.name} не может быть распределен из-за нехватки места")
        
        self.refresh_tables()
        self.update_status("Распределение грузов выполнено")
        
        # Показать результаты
        self.show_distribution_results()
        
    def show_distribution_results(self):
        window = tk.Toplevel(self.root)
        window.title("Результаты распределения")
        window.geometry("600x400")
        
        text = tk.Text(window, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Формирование отчета
        report = "РЕЗУЛЬТАТЫ РАСПРЕДЕЛЕНИЯ ГРУЗОВ\n"
        report += "=" * 50 + "\n\n"
        
        report += "ТРАНСПОРТНЫЕ СРЕДСТВА:\n"
        for transport in self.transports:
            utilization = (transport.current_load / transport.capacity * 100) if transport.capacity > 0 else 0
            report += (f"  ID: {transport.transport_id}, Тип: {transport.transport_type.value}, "
                      f"Загрузка: {transport.current_load:.1f}/{transport.capacity:.1f} кг "
                      f"({utilization:.1f}%)\n")
        
        report += "\nКЛИЕНТЫ:\n"
        for client in self.clients:
            report += f"  {client.name}: {client.cargo_weight} кг {'(VIP)' if client.is_vip else ''}\n"
        
        report += "\nОБЩАЯ СТАТИСТИКА:\n"
        total_cargo = sum(c.cargo_weight for c in self.clients)
        total_capacity = sum(t.capacity for t in self.transports)
        total_load = sum(t.current_load for t in self.transports)
        report += f"  Общий вес грузов: {total_cargo:.1f} кг\n"
        report += f"  Общая грузоподъемность: {total_capacity:.1f} кг\n"
        report += f"  Использовано: {total_load:.1f} кг ({total_load/total_capacity*100:.1f}%)\n"
        
        text.insert(tk.END, report)
        text.config(state=tk.DISABLED)
        
        # Кнопка закрытия
        ttk.Button(window, text="Закрыть", command=window.destroy).pack(pady=10)
        
    # ========== ЭКСПОРТ ДАННЫХ ==========
    
    def export_results(self):
        if not self.clients and not self.transports:
            messagebox.showwarning("Предупреждение", "Нет данных для экспорта")
            return
            
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                data = {
                    "clients": [c.to_dict() for c in self.clients],
                    "transports": [t.to_dict() for t in self.transports],
                    "next_transport_id": self.next_transport_id
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                self.update_status(f"Данные экспортированы в {os.path.basename(file_path)}")
                messagebox.showinfo("Успех", "Данные успешно экспортированы")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при экспорте: {str(e)}")
                
    # ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========
    
    def refresh_tables(self):
        # Очистка таблиц
        for tree in [self.clients_tree, self.transports_tree]:
            for item in tree.get_children():
                tree.delete(item)
        
        # Заполнение таблицы клиентов
        for client in self.clients:
            self.clients_tree.insert("", tk.END, values=(
                client.name,
                f"{client.cargo_weight:.1f}",
                "Да" if client.is_vip else "Нет"
            ))
        
        # Заполнение таблицы транспорта
        for transport in self.transports:
            self.transports_tree.insert("", tk.END, values=(
                transport.transport_id,
                transport.transport_type.value,
                f"{transport.capacity:.1f}",
                f"{transport.current_load:.1f}"
            ))
    
    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel(self.root)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0", 
                            relief=tk.SOLID, borderwidth=1, padding=5)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.after(3000, hide_tooltip)
        
        widget.bind('<Enter>', show_tooltip)
    
    def show_about(self):
        about_text = (
            "Лабораторная работа: Распределение грузов\n\n"
            "Вариант: (укажите ваш вариант)\n\n"
            "Разработчик: (укажите ваше ФИО)\n\n"
            "Функционал:\n"
            "• Управление клиентами и транспортными средствами\n"
            "• Оптимизация распределения грузов\n"
            "• Экспорт результатов в файл\n"
            "• Валидация вводимых данных"
        )
        messagebox.showinfo("О программе", about_text)

# ========== ТОЧКА ВХОДА ==========

def main():
    root = tk.Tk()
    app = CargoDistributionApp(root)
    
    # Центрирование окна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
     main()