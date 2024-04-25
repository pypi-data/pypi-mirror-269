from __future__ import annotations

import os
from typing import Any, Optional

from pydantic import BaseModel


class File(BaseModel):
    data: Any
    file_name: str
    path: Optional[str] = ""

    @classmethod
    def create(cls, data: Any, file_name: str) -> File:
        file_obj = cls(data=data, file_name=file_name)

        with open(file_name, "w") as file:
            file.write(data)

        file_obj.path = os.path.abspath(file_name)

        return file_obj
