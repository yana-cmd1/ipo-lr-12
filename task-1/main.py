#Дмитрук Яны
class Client:
    # класс клиента, у которого есть имя, вес груза и статус VIP
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = name # имя клиента
        self.cargo_weight = cargo_weight # вес груза клиента
        self.is_vip = is_vip # статус VIP