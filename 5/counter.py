"""
Написать декоратор instances_counter, который применяется к любому классу
и добавляет ему 2 метода:
get_created_instances - возвращает количество созданых экземпляров класса
reset_instances_counter - сбросить счетчик экземпляров,
возвращает значение до сброса
Имя декоратора и методов не менять

Ниже пример использования
"""


def instances_counter(cls):
    number_of_instances = 0

    class NewClass(cls):
        def __new__(cls, *args, **kwargs):
            nonlocal number_of_instances
            number_of_instances += 1
            instance = super().__new__(cls)
            return instance

        @staticmethod
        def get_created_instances():
            return number_of_instances

        @staticmethod
        def reset_instances_counter():
            nonlocal number_of_instances
            val = number_of_instances
            number_of_instances = 0
            return val

    return NewClass


@instances_counter
class User:
    pass


if __name__ == '__main__':
    User.get_created_instances()  # 0
    user, _, _ = User(), User(), User()
    user.get_created_instances()  # 3
    user.reset_instances_counter()  # 3
