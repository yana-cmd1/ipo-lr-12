import os
import sys

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем классы напрямую из файлов
try:
    # Способ 1: Импорт из папки transport
    from transport.client import Client
    from transport.vehicle import Vehicle
    from transport.van import Van
    from transport.ship import Ship
    from transport.company import TransportCompany
except ImportError:
    # Способ 2: Если transport как пакет не работает, создаем классы прямо здесь
    print("Использую встроенные классы...")
    
    class Client:
        def __init__(self, name: str, cargo_weight: float, is_vip: bool = False):
            self.name = name
            self.cargo_weight = cargo_weight
            self.is_vip = is_vip
        
        def __str__(self):
            vip = "VIP" if self.is_vip else "обычный"
            return f"Клиент: {self.name}, Груз: {self.cargo_weight}т, Статус: {vip}"
    
    class Vehicle:
        def __init__(self, capacity: float):
            import random
            import string
            self.vehicle_id = 'V' + ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
            self.capacity = capacity
            self.current_load = 0.0
            self.clients_list = []
        
        def load_cargo(self, client):
            if self.current_load + client.cargo_weight <= self.capacity:
                self.current_load += client.cargo_weight
                self.clients_list.append(client)
                return True
            return False
        
        def __str__(self):
            return f"Транспорт ID: {self.vehicle_id}, Грузоподъемность: {self.capacity}т"
    
    class Van(Vehicle):
        def __init__(self, capacity: float, is_refrigerated: bool = False):
            super().__init__(capacity)
            self.is_refrigerated = is_refrigerated
        
        def __str__(self):
            fridge = "с холодильником" if self.is_refrigerated else "без холодильника"
            return f"Фургон {fridge}, {super().__str__()}"
    
    class Ship(Vehicle):
        def __init__(self, capacity: float, name: str):
            super().__init__(capacity)
            self.name = name
        
        def __str__(self):
            return f"Судно '{self.name}', {super().__str__()}"
    
    class TransportCompany:
        def __init__(self, name: str):
            self.name = name
            self.vehicles = []
            self.clients = []
        
        def add_vehicle(self, vehicle):
            self.vehicles.append(vehicle)
            return True
        
        def add_client(self, client):
            self.clients.append(client)
            return True
        
        def optimize_cargo_distribution(self):
            print("\n=== ОПТИМИЗАЦИЯ РАСПРЕДЕЛЕНИЯ ГРУЗОВ ===")
            # Сбрасываем загрузку
            for v in self.vehicles:
                v.current_load = 0
                v.clients_list = []
            
            # Загружаем VIP клиентов
            vip_clients = [c for c in self.clients if c.is_vip]
            for client in vip_clients:
                loaded = False
                for vehicle in self.vehicles:
                    if vehicle.load_cargo(client):
                        print(f"✓ VIP {client.name} загружен в {vehicle.vehicle_id}")
                        loaded = True
                        break
                if not loaded:
                    print(f"✗ Не удалось загрузить VIP {client.name}")
            
            # Загружаем обычных клиентов
            regular_clients = [c for c in self.clients if not c.is_vip]
            for client in regular_clients:
                loaded = False
                for vehicle in self.vehicles:
                    if vehicle.load_cargo(client):
                        print(f"✓ {client.name} загружен в {vehicle.vehicle_id}")
                        loaded = True
                        break
                if not loaded:
                    print(f"✗ Не удалось загрузить {client.name}")
            
            print(f"\nИспользовано транспорта: {sum(1 for v in self.vehicles if v.clients_list)} из {len(self.vehicles)}")


def main():
    """Главное меню"""
    company = None
    
    while True:
        print("\n" + "="*50)
        print("ТРАНСПОРТНАЯ КОМПАНИЯ")
        print("="*50)
        if company:
            print(f"Компания: {company.name}")
        print("1. Создать компанию")
        print("2. Добавить клиента")
        print("3. Добавить транспорт")
        print("4. Показать клиентов")
        print("5. Показать транспорт")
        print("6. Оптимизировать грузы")
        print("7. Тестовые данные")
        print("0. Выход")
        print("="*50)
        
        choice = input("Выберите: ")
        
        if choice == '0':
            break
        
        elif choice == '1':
            name = input("Название компании: ")
            company = TransportCompany(name)
            print(f" Компания '{name}' создана!")
        
        elif choice == '2':
            if not company:
                print(" Сначала создайте компанию!")
                continue
            
            name = input("Имя клиента: ")
            weight = float(input("Вес груза (т): "))
            vip = input("VIP? (y/n): ").lower() == 'y'
            
            client = Client(name, weight, vip)
            company.add_client(client)
            print(f" Клиент {name} добавлен!")
        
        elif choice == '3':
            if not company:
                print(" Сначала создайте компанию!")
                continue
            
            print("Тип транспорта:")
            print("1. Фургон")
            print("2. Судно")
            print("3. Обычный транспорт")
            type_choice = input("Выберите: ")
            
            capacity = float(input("Грузоподъемность (т): "))
            
            if type_choice == '1':
                fridge = input("Холодильник? (y/n): ").lower() == 'y'
                vehicle = Van(capacity, fridge)
            elif type_choice == '2':
                name = input("Название судна: ")
                vehicle = Ship(capacity, name)
            else:
                vehicle = Vehicle(capacity)
            
            company.add_vehicle(vehicle)
            print(f" Транспорт добавлен! ID: {vehicle.vehicle_id}")
        
        elif choice == '4':
            if not company or not company.clients:
                print(" Нет клиентов!")
            else:
                print(f"\n Клиенты ({len(company.clients)}):")
                for client in company.clients:
                    print(f"  • {client}")
        
        elif choice == '5':
            if not company or not company.vehicles:
                print(" Нет транспорта!")
            else:
                print(f"\n Транспорт ({len(company.vehicles)}):")
                for vehicle in company.vehicles:
                    print(f"  • {vehicle}")
        
        elif choice == '6':
            if not company:
                print(" Сначала создайте компанию!")
            elif not company.clients:
                print(" Нет клиентов!")
            elif not company.vehicles:
                print(" Нет транспорта!")
            else:
                company.optimize_cargo_distribution()
        
        elif choice == '7':
            if not company:
                company = TransportCompany("Тестовая компания")
            
            # Тестовые данные
            clients = [
                Client("Иванов Иван", 5.0, True),
                Client("Петров Петр", 3.0),
                Client("Сидорова Анна", 8.0, True),
                Client("Кузнецов Алексей", 2.0),
                Client("Смирнова Мария", 4.5),
            ]
            
            vehicles = [
                Van(10.0, True),
                Ship(15.0, "Морской волк"),
                Vehicle(8.0),
            ]
            
            for client in clients:
                company.add_client(client)
            
            for vehicle in vehicles:
                company.add_vehicle(vehicle)
            
            print(" Тестовые данные загружены!")
        
        else:
            print(" Неверный выбор!")


if __name__ == "__main__":
    main()