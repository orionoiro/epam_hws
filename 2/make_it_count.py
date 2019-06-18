counter_name = 'var'
global_name = None
d = locals().copy()

for key in d:
    if d[key] == 'var':
        global_name = str(key)


def make_it_count(func, global_name):
    def func_increment():
        global counter_name
        counter_name += global_name
        func()

    return func_increment
