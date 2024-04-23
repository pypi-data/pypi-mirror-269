import decimal


def Decimal(x):
    return decimal.Decimal(str(x))

def add(x, y, unit):
    return (round(x / unit) + round(y / unit)) * unit

def substract(x, y, unit):
    return (round(x / unit) - round(y / unit)) * unit

def multiply(x, y, unit):
    return float(Decimal(x) * Decimal(y))

def divide(x, y, unit):
    return float(Decimal(x) / Decimal(y))