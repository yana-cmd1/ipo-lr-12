from .vehicle import Vehicle

class Van(Vehicle):
    def __init__(self, capacity: float, is_refrigerated: bool = False):
        super().__init__(capacity)
        self.is_refrigerated = is_refrigerated
        self.vehicle_id = 'F' + self.vehicle_id[1:]
    
    def __str__(self):
        fridge = "с холодильником" if self.is_refrigerated else "без холодильника"
        return f"Фургон {fridge}, {super().__str__()}"
    
    def __repr__(self):
        return f"Van('{self.vehicle_id}', {self.capacity}, {self.is_refrigerated})"