#Дмитрук Яны
# -*- coding: utf-8 -*-  # указываем кодировку файла, чтобы поддерживалась кириллица
import dearpygui.dearpygui as dpg   
from transport import Client, Airplane, Van, TransportCompany  
from task_3(lr-13)import *
company = TransportCompany("Белтранс")   

def log_message(msg: str):  # функция для вывода сообщений в окно "Вывод"
    dpg.set_value("output_text", msg)   

# --- Callbacks ---
def show_clients_callback(sender, app_data):   
    if company.clients:   
        text = "\n".join(str(c) for c in company.clients)   
        log_message(text)   
    else:
        log_message("Список клиентов пуст.")   

def show_vehicles_callback(sender, app_data):  
    if company.vehicles:  # Если список транспорта не пуст
        text = "\n".join(str(v) for v in company.vehicles)   
        log_message(text)   
    else:
        log_message("Список транспорта пуст.")   

def add_client_callback(sender, app_data):   
    name = dpg.get_value("client_name").strip()  
    if not name:  # Проверяем, что имя не пустое
        log_message("Ошибка: имя клиента не может быть пустым.")  
        return
    try:
        weight = float(dpg.get_value("client_weight"))  # получаем вес груза и преобразуем в число
    except (TypeError, ValueError):
        log_message("Ошибка: вес должен быть числом.")   
        return
    vip = bool(dpg.get_value("client_vip"))  # получаем статус VIP из чекбокса
    try:
        company.add_client(Client(name, weight, vip))   
    except Exception as e:
        log_message(f"Ошибка добавления клиента: {e}")   
        return
    log_message(f"Клиент {name} добавлен.")   

def delete_client_callback(sender, app_data):   
    name = dpg.get_value("delete_client_name").strip()  # получаем имя клиента для удаления
    if not name:
        log_message("Введите имя клиента для удаления.")   
        return
    found = False  
    for c in list(company.clients):  
        if c.name == name:   
            company.clients.remove(c)   
            log_message(f"Клиент {name} удалён.")   
            found = True
            break
    if not found:
        log_message(f"Клиент {name} не найден.")   

def optimize_callback(sender, app_data):  
    try:
        result = company.optimize_cargo_distribution()  
    except Exception as e:
        log_message(f"Ошибка распределения: {e}")   
        return
    log_message(result)  

def save_results_callback(sender, app_data):   
    try:
        result = company.optimize_cargo_distribution()   
        with open("distribution_results.txt", "w", encoding="utf-8") as f:   
            f.write(result)  # Записываем результат в файл
        log_message("Результаты сохранены в distribution_results.txt")   
    except Exception as e:
        log_message(f"Ошибка сохранения: {e}")  

def add_airplane_callback(sender, app_data):  
    try:
        cap = float(dpg.get_value("airplane_capacity"))  # получаем грузоподъёмность
        alt = int(dpg.get_value("airplane_altitude"))    # получаем высоту и приводим к целому числу
    except (TypeError, ValueError):
        log_message("Ошибка: грузоподъёмность и высота должны быть числами.")   
        return
    try:
        company.add_vehicle(Airplane(cap, alt))  # создаём самолёт и добавляем в компанию
    except Exception as e:
        log_message(f"Ошибка добавления самолёта: {e}")  # если ошибка, выводим её
        return
    log_message("Самолёт добавлен.")   
def add_van_callback(sender, app_data):  
    try:
        cap = float(dpg.get_value("van_capacity"))  # получаем грузоподъёмность
    except (TypeError, ValueError):
        log_message("Ошибка: грузоподъёмность должна быть числом.")   
        return
    refr = bool(dpg.get_value("van_refrigerator"))   
    try:
        company.add_vehicle(Van(cap, refr))   
    except Exception as e:
        log_message(f"Ошибка добавления фургона: {e}")   
        return
    log_message("Фургон добавлен.")  

# --- GUI ---
dpg.create_context()  

# подключаем шрифт с поддержкой кириллицы
with dpg.font_registry():  
    with dpg.font("D:/python/ipo-lr-12/DejaVuSans.ttf", 16) as default_font: 
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)  
dpg.bind_font(default_font)  

# Главное окно управления
with dpg.window(label="Управление транспортной компанией", width=600, height=680, pos=(0, 0)): 
    dpg.add_text("Меню управления")  

    dpg.add_button(label="Вывести записи клиентов", callback=show_clients_callback)  
    dpg.add_button(label="Вывести список транспорта", callback=show_vehicles_callback)  

    dpg.add_separator() 
    dpg.add_input_text(label="Имя клиента", tag="client_name", width=250)   
    dpg.add_input_text(label="Вес груза (тонн)", tag="client_weight", width=250)  
    dpg.add_checkbox(label="VIP клиент", tag="client_vip")   
    dpg.add_button(label="Добавить клиента", callback=add_client_callback)   

    dpg.add_separator()
    dpg.add_input_text(label="Имя клиента для удаления", tag="delete_client_name", width=250)   
    dpg.add_button(label="Удалить клиента", callback=delete_client_callback)  

    dpg.add_separator()
    dpg.add_button(label="Распределить грузы", callback=optimize_callback)   
    dpg.add_button(label="Сохранить результаты в файл", callback=save_results_callback)   

    dpg.add_separator()
    dpg.add_input_text(label="Грузоподъёмность самолёта", tag="airplane_capacity", width=250)   
    dpg.add_input_text(label="Макс. высота полёта (м)", tag="airplane_altitude", width=250)  
    dpg.add_button(label="Добавить самолёт", callback=add_airplane_callback)  

    dpg.add_separator()
    dpg.add_input_text(label="Грузоподъёмность фургона", tag="van_capacity", width=250)  
    dpg.add_checkbox(label="Есть холодильник", tag="van_refrigerator")   
    dpg.add_button(label="Добавить фургон", callback=add_van_callback)  

# Окно вывода результатов
with dpg.window(label="Вывод", width=620, height=680, pos=(620, 0)):  
    dpg.add_text("Здесь будут результаты", tag="output_text", wrap=600)  

# Viewport и цикл приложения
dpg.create_viewport(title="Белтранс GUI", width=1260, height=720) 
dpg.setup_dearpygui()   
dpg.show_viewport()     
dpg.start_dearpygui()   
dpg.destroy_context()   
