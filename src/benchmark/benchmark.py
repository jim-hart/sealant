from __future__ import print_function
from functools import wraps

import time
import sys

"""Simple bechmark decorator to be used as needed"""

def benchmark(function_):
    """Decorator for benchmarking string creation time.  Useful for large string
    blocks"""

    @wraps(function_)
    def function_wrapper(*args, **kwargs):
        print("Function : {}()".format(function_.__name__))
        print("Benchmark: ", end='')
        sys.stdout.flush()

        start = time.time()
        result = function_(*args, **kwargs)
        print("{:4.3f}s".format(time.time() - start))

        return result

    return function_wrapper