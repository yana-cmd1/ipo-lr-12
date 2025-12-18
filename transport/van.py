from .vehicle import Vehicle

class Van(Vehicle):
    def __init__(self, capacity: float, is_refrigerated: bool = False):
          super().__init__(capacity)  # вызываем конструктор родителя Vehicle
        if not isinstance(is_refrigerated, bool):  # добавлена проверка типа
            raise TypeError("is_refrigerated должен быть True или False")
        self.is_refrigerated = is_refrigerated  # сохраняем признак наличия холодильника
        
    def __str__(self):
        return super().__str__() + f"\nХолодильник: {self.is_refrigerator}" # параметр холодильника
