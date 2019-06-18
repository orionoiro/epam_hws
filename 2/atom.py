def atom(variable=None):
    atom.variable = variable

    def get_value():
        return atom.variable

    def set_value(value):
        atom.variable = value
        return atom.variable

    def process_value(*args):
        for elem in args:
            atom.variable = elem(atom.variable)
        return atom.variable

    def delete_value():
        del atom.variable

    return get_value, set_value, process_value, delete_value
