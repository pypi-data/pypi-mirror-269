import logging
import logging.handlers
import os
from typing import Literal, Required, TypedDict

import httpx

from loggerk.formatters import Formatter

LoggingLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BaseHandlerDictConfig(TypedDict):
    class_: Required[
        Literal[
            "logging.FileHandler",
            "logging.StreamHandler",
            "logging.handlers.QueueHandler",
            "logging.handlers.MemoryHandler",
            "logging.handlers.SocketHandler",
            "logging.handlers.SysLogHandler",
            "logging.handlers.HTTPHandler",
            "logging.handlers.DatagramHandler",
            "logging.handlers.BufferingHandler",
            "logging.handlers.NTEventLogHandler",
            "logging.handlers.WatchedFileHandler",
            "logging.handlers.RotatingFileHandler",
            "logging.handlers.TimedRotatingFileHandler",
        ]
    ]
    formatter: Required[Formatter]
    level: Required[LoggingLevel]


class FileHandlerDictConfig(BaseHandlerDictConfig, TypedDict, total=True):
    filename: Required[str]
    mode: Required[Literal["w", "a", "wb", "ab"]]
    maxBytes: int
    backupCount: int


class StreamHandlerDictConfig(BaseHandlerDictConfig, TypedDict, total=True):
    stream: Required[Literal["ext://sys.stderr"]]
    level: Required[LoggingLevel]


class HTTPHandlerDictConfig(BaseHandlerDictConfig, TypedDict, total=True):
    class_: Literal["logging.handlers.HTTPHandler"] = "logging.handlers.HTTPHandler"
    host: Required[str]
    url: Required[str]
    method: Required[Literal["GET", "POST"]]
    secure: bool
    credentials: Required[str]


def new_http_handler(
    host: str,
    url: str,
    method: Literal["GET", "POST"],
    secure: bool,
    credentials: str,
    formatter: Literal["simple", "complex"] = "simple",
    level: LoggingLevel = "DEBUG",
) -> HTTPHandlerDictConfig:
    return HTTPHandlerDictConfig(
        class_="logging.handlers.HTTPHandler",
        formatter=formatter,
        level=level,
        host=host,
        url=url,
        method=method,
        secure=secure,
        credentials=credentials,
    )


def new_file_handler(
    filename: str,
    mode: Literal["w", "a", "wb", "ab"] = "w",
    maxBytes: int = 100000,
    backupCount: int = 10,
    level: LoggingLevel = "DEBUG",
    formatter: Literal["simple", "complex"] = "simple",
) -> FileHandlerDictConfig:
    return FileHandlerDictConfig(
        class_="logging.handlers.RotatingFileHandler",
        formatter=formatter,
        level=level,
        filename=filename,
        mode=mode,
        maxBytes=maxBytes,
        backupCount=backupCount,
    )


class CustomHTTPHandler(logging.Handler):
    app_name: str

    def __init__(
        self,
        app_name: str,
        auth: Literal["Basic", "Bearer", None] = "Bearer",
        credentials: str = None,
        urls: list[str] = None,
        method: Literal["GET", "POST"] = "POST",
        level: LoggingLevel = "DEBUG",
    ) -> None:
        self.app_name = app_name
        if urls is None:
            urls = os.getenv("LOGGER_URLS")
            self.urls = urls.split(",") if urls else []
            if not self.urls:
                raise ValueError(
                    "URLs are required, either pass it as an argument or set the LOGGER_URLS environment variable"
                )

        if auth:
            if credentials is None:
                credentials = os.getenv("LOGGER_CREDENTIALS")
                if not credentials:
                    raise ValueError(
                        "credentials is required, either pass it as an argument or set the LOGGER_CREDENTIALS environment variable"
                    )
                credentials = f"{auth} {credentials}"

        self.credentials = credentials
        self.method = method
        self.level = level
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        for url in self.urls:
            try:
                response = httpx.request(
                    method=self.method,
                    url=url,
                    params={
                        "microservice": self.app_name,
                    },
                    json=log_entry,
                    headers={
                        "Authorization": f"{self.credentials}",
                    },
                )
                if not response.is_success:
                    continue
                return
            except (
                httpx._exceptions.ConnectTimeout,
                httpx._exceptions.ConnectError,
            ) as e:
                # print(f"Error: {e}")
                continue

        # raise ConnectionError("Failed to send log entry to any of the URLs")
