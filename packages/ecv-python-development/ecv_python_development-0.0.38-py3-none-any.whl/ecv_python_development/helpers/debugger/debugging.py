import functools
import inspect
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
        class_name = (
            func.__qualname__.split(".")[0] if "." in func.__qualname__ else None
        )
        print(
            f"CLASS_NAME: {class_name} | FUNCTION_NAME: {func.__name__} | FUNCTION_DURATION: {duration:.6f} seconds."
        )
        return result

    return wrapper


def decorate_all_with(decorator, predicate=None):
    """Apply a decorator to all methods that satisfy a predicate, if given."""

    if predicate is None:
        predicate = lambda _: True

    def decorate_all(cls):
        for name, method in inspect.getmembers(
            cls, predicate=lambda x: inspect.isfunction(x) or isclassmethod(x)
        ):
            if predicate(method) and method.__qualname__.startswith(cls.__name__ + "."):
                setattr(cls, name, decorator(method))

        return cls

    return decorate_all


def isclassmethod(method):
    bound_to = getattr(method, "__self__", None)
    if not isinstance(bound_to, type):
        # must be bound to a class
        return False
    name = method.__name__
    for cls in bound_to.__mro__:
        descriptor = vars(cls).get(name)
        if descriptor is not None:
            return isinstance(descriptor, classmethod)
    return False


def debug_disable(function):
    function.debug = True
    return function


def debug_enabled(function):
    try:
        return not bool(function.debug)
    except AttributeError:
        return True
