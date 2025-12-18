# -*- coding: utf-8 -*-  # указываем кодировку файла, чтобы поддерживалась кириллица
import dearpygui.dearpygui as dpg
from transport import Client, Airplane, Van, TransportCompany
from task_3(lr-13_) import *

company = TransportCompany("Белтранс")

def log_message(msg: str):
    dpg.set_value("output_text", msg)

# --- callbacks ---
def show_clients_callback(sender, app_data): # колбэк для кнопки "Вывести записи клиентов"
    if company.clients:
        text = "\n".join(str(c) for c in company.clients)
        log_message(text)
    else:
        log_message("список клиентов пуст.")

def show_vehicles_callback(sender, app_data):
    if company.vehicles:
        text = "\n".join(str(v) for v in company.vehicles)
        log_message(text)
    else:
        log_message("список транспорта пуст.")

def add_client_callback(sender, app_data): # колбэк для добавления клиента
    name = dpg.get_value("client_name").strip()
    if not name:
        log_message("ошибка: имя клиента не может быть пустым.")
        return
    try:
        weight = float(dpg.get_value("client_weight"))
    except (TypeError, ValueError):
        log_message("ошибка: вес должен быть числом.")
        return
    vip = bool(dpg.get_value("client_vip"))
    try:
        company.add_client(Client(name, weight, vip))
    except Exception as e:
        log_message(f"ошибка добавления клиента: {e}")
        return
    log_message(f"клиент {name} добавлен.")

def delete_client_callback(sender, app_data): # колбэк для удаления клиента
    name = dpg.get_value("delete_client_name").strip()
    if not name:
        log_message("введите имя клиента для удаления.")
        return
    found = False
    for c in list(company.clients):
        if c.name == name:
            company.clients.remove(c)
            log_message(f"клиент {name} удалён.")
            found = True
            break
    if not found:
        log_message(f"клиент {name} не найден.")

def optimize_callback(sender, app_data): # колбэк для распределения грузов
    try:
        result = company.optimize_cargo_distribution()
    except Exception as e:
        log_message(f"ошибка распределения: {e}")
        return
    log_message(result)

def add_airplane_callback(sender, app_data): # колбэк для добавления самолёта
    try:
        cap = float(dpg.get_value("airplane_capacity"))
        alt = int(dpg.get_value("airplane_altitude"))
    except (TypeError, ValueError):
        log_message("ошибка: грузоподъёмность и высота должны быть числами.")
        return
    try:
        company.add_vehicle(Airplane(cap, alt))
    except Exception as e:
        log_message(f"ошибка добавления самолёта: {e}")
        return
    log_message("самолёт добавлен.")

def add_van_callback(sender, app_data):# колбэк для добавления фургона
    try:
        cap = float(dpg.get_value("van_capacity"))
    except (TypeError, ValueError):
        log_message("ошибка: грузоподъёмность должна быть числом.")
        return
    refr = bool(dpg.get_value("van_refrigerator"))
    try:
        company.add_vehicle(Van(cap, refr))
    except Exception as e:
        log_message(f"ошибка добавления фургона: {e}")
        return
    log_message("фургон добавлен.")

# --- gui ---
dpg.create_context()

# подключение шрифта с поддержкой кириллицы
with dpg.font_registry():
    with dpg.font("D:/python/ipo-lr-12/DejaVuSans.ttf", 16) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font(default_font)

# главное окно управления
with dpg.window(label="управление транспортной компанией", width=600, height=680, pos=(0, 0)):
    dpg.add_text("меню управления")
    dpg.add_button(label="вывести записи клиентов", callback=show_clients_callback)
    dpg.add_button(label="вывести список транспорта", callback=show_vehicles_callback)
    
    dpg.add_separator()
    dpg.add_input_text(label="имя клиента", tag="client_name", width=250)
    dpg.add_input_text(label="вес груза (тонн)", tag="client_weight", width=250)
    dpg.add_checkbox(label="vip клиент", tag="client_vip")
    dpg.add_button(label="добавить клиента", callback=add_client_callback)
    
    dpg.add_separator()
    dpg.add_input_text(label="имя клиента для удаления", tag="delete_client_name", width=250)
    dpg.add_button(label="удалить клиента", callback=delete_client_callback)
    
    dpg.add_separator()
    dpg.add_button(label="распределить грузы", callback=optimize_callback)
    dpg.add_button(label="сохранить результаты в файл", callback=save_results_callback)
    
    dpg.add_separator()
    dpg.add_input_text(label="грузоподъёмность самолёта", tag="airplane_capacity", width=250)
    dpg.add_input_text(label="макс. высота полёта (м)", tag="airplane_altitude", width=250)
    dpg.add_button(label="добавить самолёт", callback=add_airplane_callback)
    
    dpg.add_separator()
    dpg.add_input_text(label="грузоподъёмность фургона", tag="van_capacity", width=250)
    dpg.add_checkbox(label="есть холодильник", tag="van_refrigerator")
    dpg.add_button(label="добавить фургон", callback=add_van_callback)

# окно вывода результатов
with dpg.window(label="вывод", width=620, height=680, pos=(620, 0)):
    dpg.add_text("здесь будут результаты", tag="output_text", wrap=600)

# Viewport и цикл приложения
dpg.create_viewport(title="Белтранс GUI", width=1260, height=720)  # создаём окно приложения
dpg.setup_dearpygui()  # настраиваем DearPyGui
dpg.show_viewport()    # показываем окно
dpg.start_dearpygui()  # запускаем главный цикл приложения
dpg.destroy_context()  # кничтожаем контекст после закрытия



