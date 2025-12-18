from .vehicle import Vehicle

class Ship(Vehicle):
    def __init__(self, capacity: float, name: str):
        super().__init__(capacity)
        self.name = name
        self.vehicle_id = 'S' + self.vehicle_id[1:]
    
    def __str__(self):
        return f"Судно '{self.name}', {super().__str__()}"
    
    def __repr__(self):
        return f"Ship('{self.vehicle_id}', '{self.name}', {self.capacity})"