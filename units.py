SERVING = 's'


AS_GRAMS = {
    'g': 1.0,
    'lb': 453.592
}


def as_grams(amount, unit):
    return amount * AS_GRAMS[unit]
