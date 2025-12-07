from .client import Client
from .vehicle import Vehicle
from .van import Van
from .ship import Ship

class TransportCompany:
    def __init__(self, name: str):
        self.name = name
        self.vehicles = []
        self.clients = []
    
    def add_vehicle(self, vehicle: Vehicle) -> bool:
        if not isinstance(vehicle, Vehicle):
            print(f"Ошибка: ожидается Vehicle, получен {type(vehicle).__name__}")
            return False
        
        if any(v.vehicle_id == vehicle.vehicle_id for v in self.vehicles):
            print(f"Ошибка: транспорт с ID {vehicle.vehicle_id} уже существует")
            return False
        
        self.vehicles.append(vehicle)
        return True
    
    def add_client(self, client: Client) -> bool:
        if not isinstance(client, Client):
            print(f"Ошибка: ожидается Client, получен {type(client).__name__}")
            return False
        
        self.clients.append(client)
        return True
    
    def list_vehicles(self):
        return [str(vehicle) for vehicle in self.vehicles]
    
    def optimize_cargo_distribution(self):
        for vehicle in self.vehicles:
            vehicle.current_load = 0.0
            vehicle.clients_list = []
        
        vip_clients = [c for c in self.clients if c.is_vip]
        regular_clients = [c for c in self.clients if not c.is_vip]
        
        vip_clients.sort(key=lambda c: c.cargo_weight, reverse=True)
        regular_clients.sort(key=lambda c: c.cargo_weight, reverse=True)
        self.vehicles.sort(key=lambda v: v.capacity, reverse=True)
        
        results = {
            'total_clients': len(self.clients),
            'loaded_clients': 0,
            'unloaded_clients': 0,
            'vehicle_usage': {}
        }
        
        print("\n=== Загрузка VIP-клиентов ===")
        for client in vip_clients:
            loaded = False
            for vehicle in self.vehicles:
                if vehicle.can_load(client.cargo_weight):
                    if vehicle.load_cargo(client):
                        print(f"✓ {client.name} загружен в {vehicle.vehicle_id}")
                        results['loaded_clients'] += 1
                        loaded = True
                        break
            
            if not loaded:
                print(f"✗ Не удалось загрузить VIP-клиента {client.name}")
                results['unloaded_clients'] += 1
        
        print("\n=== Загрузка обычных клиентов ===")
        for client in regular_clients:
            loaded = False
            for vehicle in self.vehicles:
                if vehicle.can_load(client.cargo_weight):
                    if vehicle.load_cargo(client):
                        print(f"✓ {client.name} загружен в {vehicle.vehicle_id}")
                        results['loaded_clients'] += 1
                        loaded = True
                        break
            
            if not loaded:
                print(f"✗ Не удалось загрузить клиента {client.name}")
                results['unloaded_clients'] += 1
        
        print("\n=== Использование транспорта ===")
        used_vehicles = 0
        for vehicle in self.vehicles:
            if vehicle.clients_list:
                used_vehicles += 1
                print(f"  {vehicle.vehicle_id}: {len(vehicle.clients_list)} клиентов")
        
        print(f"\nИспользовано транспорта: {used_vehicles} из {len(self.vehicles)}")
        print(f"Загружено клиентов: {results['loaded_clients']} из {results['total_clients']}")
        
        return results
    
    def __str__(self):
        return f"Компания: {self.name}, Клиентов: {len(self.clients)}, Транспорта: {len(self.vehicles)}"