from .client import Client
from .vehicle import Vehicle
 

class TransportCompany:
    # класс транспортной компании
    def __init__(self, name):
        if not isinstance(name, str):  # добавлена проверка типа имени компании
            raise TypeError("Название компании должно быть строкой")
        self.name = name  # сохраняем название компании
        self.vehicles = []   
        self.clients = []   

    def add_vehicle(self, vehicle):
        # метод добавления транспорта
        if not isinstance(vehicle, Vehicle):  # добавлена строгая проверка типа
            raise TypeError("Объект не является транспортным средством")
        self.vehicles.append(vehicle)  # добавляем транспорт в список

    def list_vehicles(self):
        # метод возвращает список всех транспортных средств
        return self.vehicles

    def add_client(self, client):
        # ммтод добавления клиента
        if not isinstance(client, Client):  # добавлена строгая проверка типа
            raise TypeError("Объект не является клиентом")
        self.clients.append(client)  # добавляем клиента в список

    def optimize_cargo_distribution(self):
        # ьетод оптимизации распределения грузов
        sorted_clients = sorted(self.clients, key=lambda c: not c.is_vip)  # VIP-клиенты первыми
        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.capacity, reverse=True)  # сортируем транспорт по вместимости

        for client in sorted_clients:
            loaded = False  
            for vehicle in sorted_vehicles:
                try:
                    vehicle.load_cargo(client)   
                    loaded = True
                    break  
                except ValueError:
                    continue   
            if not loaded:
                print(f"Не удалось загрузить клиента {client.name}: груз превышает вместимость всех транспортов")

    def __str__(self):
        # магический метод для строкового представления компании
        return (f"Транспортная компания: {self.name}\n"
                f"Количество транспортных средств: {len(self.vehicles)}\n"
                f"Количество клиентов: {len(self.clients)}")
