import transoprt *

def save_results_callback(sender, app_data):  # новый колбэк для сохранения результатов в файл
    try:
        result = company.optimize_cargo_distribution()   
        with open("distribution_results.txt", "w", encoding="utf-8") as f: 
            f.write(result)  # звписываем результат в файл
        log_message("Результаты сохранены в distribution_results.txt")  
    except Exception as e:
        log_message(f"Ошибка сохранения: {e}")   
