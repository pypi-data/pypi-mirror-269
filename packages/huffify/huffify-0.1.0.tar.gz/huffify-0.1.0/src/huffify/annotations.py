from typing import TypedDict


class FinalDataSet(TypedDict):
    table: dict[str, str]
    message: bytearray
