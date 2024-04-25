from typing import Literal, TypedDict

Formatter = Literal["simple", "complex"]


class Format(TypedDict, total=True):
    time: str
    service: str
    logLevel: str
    module: str
    pathname: str
    line: int
    message: str


class BaseFormatter(TypedDict, total=True):
    format: str
    datefmt: str