import functools


def sum_square_difference(numbers):
    return sum(numbers) ** 2 - sum([num ** 2 for num in numbers])


def pythagorean_triplet(the_sum):
    return [(m ** 2 - n ** 2) * 2 * m * n * (m ** 2 + n ** 2) for m in range(1000) for n in range(1000) if
            m * (n + m) == the_sum / 2 and m > n][0]


def self_power(number):
    return str(sum([num ** num for num in range(1, number)]))[-10::]


def champernownes_constant():
    return functools.reduce(lambda x, y: x * y,
                            [int(f'0.{"".join([str(x) for x in range(1, 1000000)])}'[indx + 1]) for indx in
                             [10 ** p for p in range(7)]])

print(sum_square_difference(range(101)))
print(pythagorean_triplet(1000))
print(self_power(1000))
print(champernownes_constant())