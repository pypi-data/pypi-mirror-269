from __future__ import annotations

import logging
import os
import typing

from enum import IntEnum

if typing.TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any, Self


class LogLevel(IntEnum):
	DEBUG = logging.DEBUG
	VERBOSE = 15
	INFO = logging.INFO
	WARNING = logging.WARNING
	ERROR = logging.ERROR
	CRITICAL = logging.CRITICAL


	def __str__(self) -> str:
		return self.name


	@classmethod
	def parse(cls: type[Self], data: Any) -> Self:
		try:
			data = int(data)

		except ValueError:
			pass

		if isinstance(data, cls):
			return data

		if isinstance(data, str):
			data = data.upper()

		try:
			return cls[data]

		except KeyError:
			pass

		try:
			return cls(data)

		except ValueError:
			pass

		raise AttributeError(f"Invalid enum property for {cls.__name__}: {data}")


class Logger(logging.Logger):
	def __init__(self, name: str):
		logging.Logger.__init__(self, name, level = LogLevel.INFO)


	def verbose(self, message: str, *args: Any, **kwargs: Any) -> None:
		if not self.isEnabledFor(LogLevel.VERBOSE):
			return

		self.log(LogLevel["VERBOSE"], message, *args, **kwargs)


if os.environ.get("INVOCATION_ID"):
	logging_format = "%(levelname)s: %(message)s"

else:
	logging_format = "[%(asctime)s] %(levelname)s: %(message)s"


logging.setLoggerClass(Logger)
logging.addLevelName(LogLevel.VERBOSE, "VERBOSE")
logging.basicConfig(
	level = LogLevel.INFO,
	format = logging_format,
	datefmt = "%Y-%m-%d %H:%M:%S",
	handlers = [logging.StreamHandler()]
)

logger: Logger = logging.getLogger("gemi") # type: ignore


def get_level() -> LogLevel:
	return LogLevel.parse(logger.level)


def set_level(level: LogLevel | str) -> None:
	logger.setLevel(LogLevel.parse(level))


debug: Callable[..., Any] = logger.debug
verbose: Callable[..., Any] = logger.verbose
info: Callable[..., Any] = logger.info
warning: Callable[..., Any] = logger.warning
error: Callable[..., Any] = logger.error
critical: Callable[..., Any] = logger.critical
