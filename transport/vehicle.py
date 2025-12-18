import random
import string

class Vehicle:
    def __init__(self, capacity: float):
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