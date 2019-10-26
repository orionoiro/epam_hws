"""
С помощью паттерна "Цепочка обязанностей" составьте список покупок для выпечки блинов.
Необходимо осмотреть холодильник и поочередно проверить, есть ли у нас необходимые ингридиенты:
    2 яйца
    300 грамм муки
    0.5 л молока
    100 грамм сахара
    10 мл подсолнечного масла
    120 грамм сливочного масла

В итоге мы должны получить список недостающих ингридиентов.
"""


class Refrigerator:
    def __init__(self, eggs, flour, milk, sugar, oil, butter):
        self.eggs = eggs
        self.flour = flour
        self.milk = milk
        self.sugar = sugar
        self.oil = oil
        self.butter = butter
        self.missing_products = []

    def check_missing(self):
        if not self.missing_products:
            print('We have everything for cooking!')
        else:
            print(self.missing_products)


class Checker:
    def set_next(self, next_check):
        pass

    def check(self):
        pass


class BaseCheck(Checker):
    def __init__(self, refrigerator):
        self.refrigerator = refrigerator

    def set_next(self, next_check):
        return next_check(self.refrigerator).check()

    def check(self):
        pass


class EggsCheck(BaseCheck):
    def check(self):
        if self.refrigerator.eggs < 2:
            self.refrigerator.missing_products.append(f'{2 - self.refrigerator.eggs} {"eggs" if 2 - self.refrigerator.eggs > 2 else "egg"}')
        return self.set_next(FlourCheck)


class FlourCheck(BaseCheck):
    def check(self):
        if self.refrigerator.flour < 0.300:
            self.refrigerator.missing_products.append(f'{round(0.300 - self.refrigerator.flour, 3)}g of flour')
        return self.set_next(MilkCheck)


class MilkCheck(BaseCheck):
    def check(self):
        if self.refrigerator.milk < 0.500:
            self.refrigerator.missing_products.append(f'{round(0.500 - self.refrigerator.milk, 3)}ml of milk')
        return self.set_next(SugarCheck)


class SugarCheck(BaseCheck):
    def check(self):
        if self.refrigerator.sugar < 0.100:
            self.refrigerator.missing_products.append(f'{round(0.100 - self.refrigerator.sugar, 3)}g of sugar')
        return self.set_next(OilCheck)


class OilCheck(BaseCheck):
    def check(self):
        if self.refrigerator.oil < 0.10:
            self.refrigerator.missing_products.append(f'{round(0.10 - self.refrigerator.oil, 3)}ml of oil')
        return self.set_next(ButterCheck)


class ButterCheck(BaseCheck):
    def check(self):
        if self.refrigerator.butter < 0.120:
            self.refrigerator.missing_products.append(f'{round(0.120 - self.refrigerator.butter, 3)}g of butter')


if __name__ == '__main__':
    refr = Refrigerator(1, 0.050, 0.060, 0.070, 0.001, 0.003)
    check = EggsCheck(refr).check()
    refr.check_missing()

    print()

    refr2 = Refrigerator(10, 0.600, 0.999, 1, 0.5, 0.3)
    check2 = EggsCheck(refr).check()
    refr2.check_missing()
