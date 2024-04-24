from pprint import pprint
from typing import Any


def brpt(any: Any) -> None:
    print("\n")
    pprint(any)
    breakpoint()
