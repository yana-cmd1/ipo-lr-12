from .vehicle import Vehicle

class Airplane(Vehicle):
    # класс самолета, наследует Vehicle
     def __init__(self, capacity, max_altitude):
        super().__init__(capacity)   
        if not isinstance(max_altitude, int):  # добавлена проверка типа высоты
            raise TypeError("Максимальная высота должна быть целым числом")
        self.max_altitude = max_altitude   
     def __str__(self):
        return super().__str__() + f"\nМаксимальная высота: {self.max_altitude} м" # выводим максимальную высоту
