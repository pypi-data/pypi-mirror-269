from __future__ import annotations

import time
from datetime import datetime as dt
from typing import Optional

from pytz import timezone


class DateTime:
    date: dt
    time_format: str = "%H:%M:%S"
    date_format: str = "%Y-%m-%d"

    def __init__(
        self, date: Optional[dt] = None, selected_timezone: str = "Asia/Manila"
    ) -> None:
        instance_date: dt = date if date else dt.now()
        self.date: dt = instance_date.astimezone(timezone(selected_timezone))

    def get_datetime(self, format: str = "") -> str:
        format = format if format else self.date_format + " " + self.time_format
        return self.date.strftime(format)

    def get_date(self, format: str = "") -> str:
        format = format if format else self.date_format
        return self.date.strftime(format)

    def get_time(self, format: str = "") -> str:
        format = format if format else self.time_format
        return self.date.strftime(format)

    @classmethod
    def get_current_datetime(cls, format: str = "") -> str:
        date = cls()
        return date.get_datetime(format)

    @classmethod
    def get_current_date(cls, format: str = "") -> str:
        date = cls()
        return date.get_date(format)

    @classmethod
    def get_current_time(cls, format: str = "") -> str:
        date = cls()
        return date.get_time(format)

    @classmethod
    def get_time_diff(cls, latest_date: dt, previous_date: dt) -> str:
        diff = latest_date - previous_date
        time_diff = str(diff).split(".")[0]
        # 1 day, 23:59:59
        time_diff_array: list[str] = time_diff.split(" day, ")
        timestamp_array: list[str]

        if len(time_diff_array) > 1:
            # If has day
            additional_hours: int = int(time_diff_array[0]) * 24

            timestamp_array = time_diff_array[1].split(":")
            timestamp_array[0] = str(int(timestamp_array[0]) + additional_hours)
        else:
            timestamp_array = time_diff_array[0].split(":")

        return ":".join(str(x) for x in timestamp_array)

    @classmethod
    def get_current_unixtimestamp(cls) -> int:
        return int(time.time())

    @classmethod
    def to_datetime(cls, str_datetime: str, format: str = "") -> dt:
        return (
            dt.strptime(str_datetime, format)
            if format
            else dt.fromisoformat(str_datetime)
        )

    def __repr__(self) -> str:
        return self.get_datetime()
