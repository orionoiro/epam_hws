"""
Представьте, что вы пишите программу по формированию и выдачи комплексных обедов для сети столовых, которая стала
расширяться и теперь предлагает комплексные обеды для вегетарианцев, детей и любителей китайской кухни.

С помощью паттерна "Абстрактная фабрика" вам необходимо реализовать выдачу комплексного обеда, состоящего из трёх
позиций (первое, второе и напиток).
В файле menu.yml находится меню на каждый день, в котором указаны позиции и их принадлежность к
определенному типу блюд.

"""
from yaml import load, BaseLoader


class BuildMenu:
    def __init__(self, dishes, day_of_week):
        self.day_of_week = day_of_week
        self.dishes = dishes

    def create_first_dish(self, day_of_week, category):
        return self.dishes[day_of_week]['first_courses'][category]

    def create_second_dish(self, day_of_week, category):
        return self.dishes[day_of_week]['second_courses'][category]

    def create_drinks(self, day_of_week, category):
        return self.dishes[day_of_week]['drinks'][category]


class BuildVeganMenu(BuildMenu):

    def build_dish(self):
        return ', '.join([self.create_first_dish(self.day_of_week, 'vegan'),
                          self.create_second_dish(self.day_of_week, 'vegan'),
                          self.create_drinks(self.day_of_week, 'vegan')])


class BuildChildMenu(BuildMenu):

    def build_dish(self):
        return ', '.join([self.create_first_dish(self.day_of_week, 'child'),
                          self.create_second_dish(self.day_of_week, 'child'),
                          self.create_drinks(self.day_of_week, 'child')])


class BuildChinaMenu(BuildMenu):

    def build_dish(self):
        return ', '.join([self.create_first_dish(self.day_of_week, 'china'),
                          self.create_second_dish(self.day_of_week, 'china'),
                          self.create_drinks(self.day_of_week, 'china')])


if __name__ == '__main__':
    with open('menu.yml', 'r', encoding='utf-8') as f:
        dishes = load(f, Loader=BaseLoader)

    days = list(dishes.keys())
    for day in days:
        vegan = BuildVeganMenu(dishes, day).build_dish()
        child = BuildChildMenu(dishes, day).build_dish()
        china = BuildChinaMenu(dishes, day).build_dish()
        print(f'{day}:\n \tVegan: {vegan}\n \tChild: {child}\n \tChina: {china}')
