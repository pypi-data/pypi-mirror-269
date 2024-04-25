import functools
import time
from pprint import pprint
from typing import Any


def brpt(any: Any) -> None:
    print("\n")
    pprint(any)
    breakpoint()


def log_duration(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Function '{func.__name__}' took {duration:.6f} seconds.")
        return result

    return wrapper
