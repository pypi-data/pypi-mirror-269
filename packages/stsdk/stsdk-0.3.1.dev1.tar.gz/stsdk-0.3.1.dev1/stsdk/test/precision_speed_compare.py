
import sys

sys.path.append("/root/lingxiao/st-sdk/")
sys.path.append("/root/lingxiao/st-sdk/stsdk")

from stsdk.utils.precision import Decimal
import time
from functools import wraps


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time_ns()
        result = f(*args, **kw)
        te = time.time_ns() - ts
        print(f'func:{f.__name__} args:{args} took: {te} ns return {result}')
        return result
    return wrap

@timing
def test_decimal(x):
    return Decimal(x)

@timing
def test_float(x):
    return round(x / 0.001) * 0.001

if __name__ == "__main__":
    
    test_decimal(0.012)

    test_float(0.012)