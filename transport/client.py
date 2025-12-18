class Client:#создаём класс клиент
    def __init__(self, name, cargo_weight, is_vip=False):#создаём конструктор инит с именем, весом, и вип статусом
        self.name = name#имя клиента
        self.cargo_weight = cargo_weight#вес груза
        self.is_vip = is_vip#статус VIP (по умолчанию False)

    def __repr__(self):#создаём метод репр чтобы удобно выводить объект в консоль
         return f"Клиент {self.name}, груз: {self.cargo_weight} тонн, VIP: {self.is_vip}"
