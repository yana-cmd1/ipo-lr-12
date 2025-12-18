# -*- coding: utf-8 -*-  # Указываем кодировку файла, чтобы поддерживалась кириллица
import dearpygui.dearpygui as dpg  # Импортируем библиотеку DearPyGui
from transport import Client, Airplane, Van, TransportCompany  # Импортируем классы из пакета transport
from task_3(lr-13_)import *
company = TransportCompany("Белтранс")  # Создаём объект транспортной компании

def log_message(msg: str):  # Функция для вывода сообщений в окно "Вывод"
    dpg.set_value("output_text", msg)  # Устанавливаем текст в элемент с тегом output_text

# --- Callbacks ---
def show_clients_callback(sender, app_data):  # Колбэк для кнопки "Вывести записи клиентов"
    if company.clients:  # Если список клиентов не пуст
        text = "\n".join(str(c) for c in company.clients)  # Формируем строку со всеми клиентами
        log_message(text)  # Выводим её в окно "Вывод"
    else:
        log_message("Список клиентов пуст.")  # Если клиентов нет, выводим сообщение

def show_vehicles_callback(sender, app_data):  # Колбэк для кнопки "Вывести список транспорта"
    if company.vehicles:  # Если список транспорта не пуст
        text = "\n".join(str(v) for v in company.vehicles)  # Формируем строку со всеми транспортами
        log_message(text)  # Выводим её
    else:
        log_message("Список транспорта пуст.")  # Если транспорта нет, выводим сообщение

def add_client_callback(sender, app_data):  # Колбэк для добавления клиента
    name = dpg.get_value("client_name").strip()  # Получаем имя клиента из поля ввода
    if not name:  # Проверяем, что имя не пустое
        log_message("Ошибка: имя клиента не может быть пустым.")  # Сообщаем об ошибке
        return
    try:
        weight = float(dpg.get_value("client_weight"))  # Получаем вес груза и преобразуем в число
    except (TypeError, ValueError):
        log_message("Ошибка: вес должен быть числом.")  # Если ошибка преобразования, выводим сообщение
        return
    vip = bool(dpg.get_value("client_vip"))  # Получаем статус VIP из чекбокса
    try:
        company.add_client(Client(name, weight, vip))  # Создаём клиента и добавляем в компанию
    except Exception as e:
        log_message(f"Ошибка добавления клиента: {e}")  # Если ошибка, выводим её
        return
    log_message(f"Клиент {name} добавлен.")  # Сообщаем об успешном добавлении

def delete_client_callback(sender, app_data):  # Колбэк для удаления клиента
    name = dpg.get_value("delete_client_name").strip()  # Получаем имя клиента для удаления
    if not name:
        log_message("Введите имя клиента для удаления.")  # Если пустое имя, выводим сообщение
        return
    found = False  # Флаг найденного клиента
    for c in list(company.clients):  # Перебираем список клиентов
        if c.name == name:  # Если имя совпадает
            company.clients.remove(c)  # Удаляем клиента
            log_message(f"Клиент {name} удалён.")  # Сообщаем об удалении
            found = True
            break
    if not found:
        log_message(f"Клиент {name} не найден.")  # Если клиент не найден, выводим сообщение

def optimize_callback(sender, app_data):  # Колбэк для распределения грузов
    try:
        result = company.optimize_cargo_distribution()  # Запускаем оптимизацию
    except Exception as e:
        log_message(f"Ошибка распределения: {e}")  # Если ошибка, выводим её
        return
    log_message(result)  # Выводим результат оптимизации

def add_airplane_callback(sender, app_data):  # Колбэк для добавления самолёта
    try:
        cap = float(dpg.get_value("airplane_capacity"))  # Получаем грузоподъёмность
        alt = int(dpg.get_value("airplane_altitude"))    # Получаем высоту и приводим к целому числу
    except (TypeError, ValueError):
        log_message("Ошибка: грузоподъёмность и высота должны быть числами.")  # Сообщаем об ошибке
        return
    try:
        company.add_vehicle(Airplane(cap, alt))  # Создаём самолёт и добавляем в компанию
    except Exception as e:
        log_message(f"Ошибка добавления самолёта: {e}")  # Если ошибка, выводим её
        return
    log_message("Самолёт добавлен.")  # Сообщаем об успешном добавлении

def add_van_callback(sender, app_data):  # Колбэк для добавления фургона
    try:
        cap = float(dpg.get_value("van_capacity"))  # Получаем грузоподъёмность
    except (TypeError, ValueError):
        log_message("Ошибка: грузоподъёмность должна быть числом.")  # Сообщаем об ошибке
        return
    refr = bool(dpg.get_value("van_refrigerator"))  # Получаем наличие холодильника
    try:
        company.add_vehicle(Van(cap, refr))  # Создаём фургон и добавляем в компанию
    except Exception as e:
        log_message(f"Ошибка добавления фургона: {e}")  # Если ошибка, выводим её
        return
    log_message("Фургон добавлен.")  # Сообщаем об успешном добавлении

# --- GUI ---
dpg.create_context()  # Создаём контекст DearPyGui

# Подключаем шрифт с поддержкой кириллицы
with dpg.font_registry():  # Регистрируем шрифты
    with dpg.font("D:/python/ipo-lr-12/DejaVuSans.ttf", 16) as default_font:  # Загружаем DejaVuSans.ttf
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)  # Включаем поддержку кириллицы
dpg.bind_font(default_font)  # Привязываем шрифт как основной

# Главное окно управления
with dpg.window(label="Управление транспортной компанией", width=600, height=680, pos=(0, 0)):  # Создаём окно управления
    dpg.add_text("Меню управления")  # Заголовок окна

    dpg.add_button(label="Вывести записи клиентов", callback=show_clients_callback)  # Кнопка для вывода клиентов
    dpg.add_button(label="Вывести список транспорта", callback=show_vehicles_callback)  # Кнопка для вывода транспорта

    dpg.add_separator()  # Разделитель
    dpg.add_input_text(label="Имя клиента", tag="client_name", width=250)  # Поле ввода имени клиента
    dpg.add_input_text(label="Вес груза (тонн)", tag="client_weight", width=250)  # Поле ввода веса груза
    dpg.add_checkbox(label="VIP клиент", tag="client_vip")  # Чекбокс для VIP
    dpg.add_button(label="Добавить клиента", callback=add_client_callback)  # Кнопка добавления клиента

    dpg.add_separator()
    dpg.add_input_text(label="Имя клиента для удаления", tag="delete_client_name", width=250)  # Поле ввода имени для удаления
    dpg.add_button(label="Удалить клиента", callback=delete_client_callback)  # Кнопка удаления клиента

    dpg.add_separator()
    dpg.add_button(label="Распределить грузы", callback=optimize_callback)  # Кнопка распределения грузов
    dpg.add_button(label="Сохранить результаты в файл", callback=save_results_callback)  # Новая кнопка сохранения результатов

    dpg.add_separator()
    dpg.add_input_text(label="Грузоподъёмность самолёта", tag="airplane_capacity", width=250)  # Поле ввода грузоподъёмности самолёта
    dpg.add_input_text(label="Макс. высота полёта (м)", tag="airplane_altitude", width=250)  # Поле ввода высоты полёта
    dpg.add_button(label="Добавить самолёт", callback=add_airplane_callback)  # Кнопка добавления самолёта

    dpg.add_separator()
    dpg.add_input_text(label="Грузоподъёмность фургона", tag="van_capacity", width=250)  # Поле ввода грузоподъёмности фургона
    dpg.add_checkbox(label="Есть холодильник", tag="van_refrigerator")  # Чекбокс наличия холодильника
    dpg.add_button(label="Добавить фургон", callback=add_van_callback)  # Кнопка добавления фургона

# Окно вывода результатов
with dpg.window(label="Вывод", width=620, height=680, pos=(620, 0)):  # Создаём окно для вывода сообщений
    dpg.add_text("Здесь будут результаты", tag="output_text", wrap=600)  # Текстовый элемент для отображения логов

# Viewport и цикл приложения
dpg.create_viewport(title="Белтранс GUI", width=1260, height=720)  # Создаём окно приложения
dpg.setup_dearpygui()  # Настраиваем DearPyGui
dpg.show_viewport()    # Показываем окно
dpg.start_dearpygui()  # Запускаем главный цикл приложения
dpg.destroy_context()  # Уничтожаем контекст после закрытия


