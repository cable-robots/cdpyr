def nonzero(value):
    if value == 0:
        raise ValueError('value must be nonzero')


def nonnegative(value):
    if value < 0:
        raise ValueError('value must be nonnegative')


def positive(value):
    if value > 0:
        raise ValueError('value must be positive')
