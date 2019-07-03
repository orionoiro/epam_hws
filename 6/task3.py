"""
Реализовать дескриптор, кодирующий слова с помощью шифра Цезаря

"""


class ShiftDescriptor:
    def __init__(self, number):
        self.number = number
        self.string = ''

    def __get__(self, instance, owner):
        return self.string

    def __set__(self, instance, new_value):
        new_string = ''
        for char in new_value:
            new_char = ord(char) + self.number % 26
            if new_char > 122:
                new_char = new_char - 123 + ord('a')
            new_string += chr(new_char)
        self.string = new_string
        return self.string


class CeasarSipher:
    message = ShiftDescriptor(4)
    another_message = ShiftDescriptor(7)


a = CeasarSipher()
a.message = 'abc'
a.another_message = 'hello'

assert a.message == 'efg'
assert a.another_message == 'olssv'
