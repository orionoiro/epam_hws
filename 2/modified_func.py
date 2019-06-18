import inspect


def modified_func(func, *args, **kwargs):

    def new_func(*args2, **kwargs2):
        new_func.__name__ = f'func_{func.__name__}'

        doc = f"""A func implementation of {func.__name__ } 
        \nwith pre-applied arguments being:
        \n{", ".join(f'{key} {value}' for key, value in locals().items() if key in ('args', 'kwargs'))}
        \nsource_code:
        \n{inspect.getsource(new_func)}"""

        new_func.__doc__ = doc
        if any((args2, kwargs2)):
            nonlocal args
            nonlocal kwargs
            args += args2
            for key in kwargs2:
                kwargs[key] = kwargs2[key]

        return func(*args, **kwargs)

    return new_func
