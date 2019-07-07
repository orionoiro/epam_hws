"""
Используя паттерн "Декоратор" реализуйте возможность дополнительно добавлять к кофе
    маршмеллоу, взбитые сливки и сироп, а затем вычислить итоговую стоимость напитка.
"""


class Component:
    def get_cost(self):
        raise NotImplementedError("Override get_cost method")


class BaseCoffee(Component):
    def get_cost(self):
        return 90


class Whip(Component):
    def __init__(self, coffee):
        self._coffee = coffee

    def get_cost(self):
        return 10 + self._coffee.get_cost()


class Marshmallow(Whip):
    def get_cost(self):
        return 25 + self._coffee.get_cost()


class Syrup(Whip):
    def get_cost(self):
        return 10 + self._coffee.get_cost()


if __name__ == "__main__":
    coffee = BaseCoffee()
    coffee = Whip(coffee)
    coffee = Marshmallow(coffee)
    coffee = Syrup(coffee)
    print("Итоговая стоимость за кофе: {}".format(str(coffee.get_cost())))
