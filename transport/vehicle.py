import uuid  # модуль для генерации уникальных идентификаторов

class Vehicle:
    # базовый класс транспортного средства
    def __init__(self, capacity):
        if not isinstance(capacity, (int, float)):  # добавлена проверка типа грузоподъёмности
            raise TypeError("Грузоподъёмность должна быть числом")
        if capacity <= 0:  # добавлена проверка на положительное значение
            raise ValueError("Грузоподъёмность должна быть положительной")

        self.vehicle_id = str(uuid.uuid4())  # генерируем уникальный ID транспорта
        self.capacity = capacity  
        self.current_load = 0  
        self.clients_list = []  

    def load_cargo(self, client):
        # метод загрузки груза клиента
        if not hasattr(client, "cargo_weight"):
            raise TypeError("У клиента отсутствует атрибут cargo_weight")
        if not isinstance(client.cargo_weight, (int, float)):
            raise TypeError("Вес груза должен быть числом")
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Груз превышает грузоподъемность")

        self.current_load += client.cargo_weight   
        self.clients_list.append(client)  

    def __str__(self):
        # магический метод для строкового представления транспорта
        client_names = [c.name for c in self.clients_list]
        return (f"ID транспорта: {self.vehicle_id}\n"
                f"Грузоподъемность: {self.capacity} тонн\n"
                f"Текущая нагрузка: {self.current_load} тонн\n"
                f"Клиенты: {client_names}")
