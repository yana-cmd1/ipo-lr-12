import transoprt *

def save_results_callback(sender, app_data):  # Новый колбэк для сохранения результатов в файл
    try:
        result = company.optimize_cargo_distribution()  # Получаем распределение грузов
        with open("distribution_results.txt", "w", encoding="utf-8") as f:  # Открываем файл для записи
            f.write(result)  # Записываем результат в файл
        log_message("Результаты сохранены в distribution_results.txt")  # Сообщаем об успешном сохранении
    except Exception as e:
        log_message(f"Ошибка сохранения: {e}")  # Если ошибка, выводим её
