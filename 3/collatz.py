def collatz_steps(n):
    if int(n) != n:
        raise ValueError
    num_of_steps = 0
    if n == 1:
        return num_of_steps
    elif n % 2 == 0:
        num_of_steps += 1
        num_of_steps += collatz_steps(n / 2)
        return num_of_steps
    else:
        num_of_steps += 1
        num_of_steps += collatz_steps(3 * n + 1)
        return num_of_steps
