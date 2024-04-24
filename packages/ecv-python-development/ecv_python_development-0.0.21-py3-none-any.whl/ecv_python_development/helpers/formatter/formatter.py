from __future__ import annotations

import json
import math
from decimal import Decimal
from re import sub
from typing import Any


def peso_to_centavos(peso: float | int | str) -> int:
    if peso:
        return int(round(float(peso) * 100))
    return 0


def centavos_to_peso(
    centavos: float | int | Decimal, string_format: bool = True
) -> str | float | Decimal:
    val = Decimal(centavos) / 100 if centavos else Decimal(0)

    if string_format:
        return "{:.2f}".format(val)
    else:
        return standard_peso(val)


def standard_peso(peso: float | Decimal | str) -> float:
    return math.floor(float(peso) * 10**2) / 10**2


class obj(object):
    def __init__(self, dict_: dict[Any, Any]) -> None:
        self.__dict__.update(dict_)


def dict2obj(d: dict[Any, Any]) -> Any:
    return json.loads(json.dumps(d), object_hook=obj)


def snake_case(s: str) -> str:
    return "_".join(
        sub(
            "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", s.replace("-", " "))
        ).split()
    ).lower()


def fetch_provider_name(username: str) -> str:
    return username.split("_")[0].capitalize()


def pynamodb_attr_to_dict(attributes: dict[Any, Any]) -> dict[Any, Any]:
    # removing pk, sk and db elements
    if "PK" in attributes:
        attributes.pop("PK")
    if "SK" in attributes:
        attributes.pop("SK")
    if "EntityType" in attributes:
        attributes.pop("EntityType")
    if "GSI1_PK" in attributes:
        attributes.pop("GSI1_PK")
    if "GSI1_SK" in attributes:
        attributes.pop("GSI1_SK")
    if "GSI2_PK" in attributes:
        attributes.pop("GSI2_PK")
    if "GSI2_SK" in attributes:
        attributes.pop("GSI2_SK")

    created_at = attributes.pop("created_at")
    updated_at = attributes.pop("updated_at")

    attributes.update({"created_at": created_at})
    attributes.update({"updated_at": updated_at})
    # convert the keys to snake case
    attributes = {snake_case(k): v for k, v in attributes.items()}

    return attributes


def pluralize(word: str) -> str:
    if (
        word.endswith("s")
        or word.endswith("x")
        or word.endswith("z")
        or word.endswith("ch")
        or word.endswith("sh")
    ):
        return word + "es"
    elif word.endswith("y"):
        return word[:-1] + "ies"
    else:
        return word + "s"


def remove_unused_keys(d: dict[Any, Any], keys_to_remove: list[Any]) -> None:
    keys_to_remove_list: list[Any] = []

    for key, value in d.items():
        if key in keys_to_remove:
            if not value:
                keys_to_remove_list.append(key)

    for key in keys_to_remove_list:
        d.pop(key)
