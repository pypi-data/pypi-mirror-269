import json
from typing import Any, Literal, TypedDict

from loggerk.formatters import BaseFormatter, Format, Formatter
from loggerk.handlers import BaseHandlerDictConfig, FileHandlerDictConfig, HTTPHandlerDictConfig, StreamHandlerDictConfig



class RootLogger(TypedDict):
    handlers: list[str]
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


DEFAULT_FILE_HANDLER = FileHandlerDictConfig(
    class_="logging.handlers.RotatingFileHandler",
    formatter="simple",
    level="DEBUG",
    filename="logs/app.log",
    mode="w",
    maxBytes=100000,
    backupCount=10,
)

DEFAULT_STDOUT_HANDLER = StreamHandlerDictConfig(
    class_="logging.StreamHandler",
    formatter="simple",
    level="DEBUG",
)

DEFAULT_HTTP_HANDLER = HTTPHandlerDictConfig(
    class_="loggerk.handlers.CustomHTTPHandler",
    formatter="simple",
    level="DEBUG",
    method="POST",
    auth="Bearer",
)


DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S %z"


DEFAULT_SIMPLE_FORMATTER = BaseFormatter(
    format="%(asctime)s [%(levelname)s] %(APP_NAME)s | %(name)s <Module: %(module)s> <File: %(pathname)s:%(lineno)d> \t %(message)s",
    datefmt=DEFAULT_DATE_FORMAT,
)

DEFAULT_COMPLEX_FORMATTER = BaseFormatter(
    format=json.dumps(
        Format(
            time="%(asctime)s",
            service="%(APP_NAME)%",
            logger="%(name)s",
            logLevel="%(levelname)s",
            module="%(module)s",
            pathname="%(pathname)s",
            line="%(lineno)d",
            message="%(message)s",
        )
    ),
    datefmt=DEFAULT_DATE_FORMAT,
)



class ConfigDict(TypedDict):
    version: int
    formatters: dict[Formatter, BaseFormatter] = {
        "simple": DEFAULT_SIMPLE_FORMATTER,
        "complex": DEFAULT_COMPLEX_FORMATTER,
    }
    handlers: dict[str, BaseHandlerDictConfig] = {
        "file": DEFAULT_FILE_HANDLER,
        "stdout": DEFAULT_STDOUT_HANDLER,
    }
    root: dict[str, Any]

    @classmethod
    def new_config(
        cls,
        version: int = 1,
        formatters: dict[Formatter, BaseFormatter] = {
            "simple": DEFAULT_SIMPLE_FORMATTER,
            "complex": DEFAULT_COMPLEX_FORMATTER,
        },
        handlers: dict[str, BaseHandlerDictConfig] = {
            "file": DEFAULT_FILE_HANDLER,
            "stdout": DEFAULT_STDOUT_HANDLER,
        },
        root: dict[str, Any] = RootLogger(
            handlers=["file", "stdout"],
            level="DEBUG"
        ),
    ) -> "ConfigDict":
        return cls(
            version=version,
            formatters=formatters,
            handlers=handlers,
            root=root,
        )


DEFAULT_CONFIG = ConfigDict(
    version=1,
    formatters={
        "simple": DEFAULT_SIMPLE_FORMATTER,
        "complex": DEFAULT_COMPLEX_FORMATTER,
    },
    handlers={
        "file": DEFAULT_FILE_HANDLER,
        "stdout": DEFAULT_STDOUT_HANDLER,
        "http": DEFAULT_HTTP_HANDLER
    },
    root=RootLogger(
        handlers=["file", "stdout", "http"],
        level="DEBUG",
    ),
)
