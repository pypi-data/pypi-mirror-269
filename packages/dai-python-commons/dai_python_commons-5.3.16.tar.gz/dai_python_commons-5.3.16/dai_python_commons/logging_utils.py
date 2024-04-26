"""Functions for logging"""

from __future__ import annotations

import itertools
import json
import sys
from typing import Any, Dict

import loguru
from loguru import logger
from loguru._better_exceptions import ExceptionFormatter
from loguru._handler import Message


class LoggingUtils:  # pylint: disable=too-few-public-methods,no-member
    """
    Class that provides useful functions for logging
    """

    # Better exception: if max_length == None => no max len
    exception_formatter = ExceptionFormatter(max_length=None)  # type: ignore

    @staticmethod
    def get_logger(name: str, level: str = "INFO") -> loguru.Logger:
        """Returns a logger object"""
        logger.remove()
        logger.configure(extra={"name": name})
        logger.add(LoggingUtils._sink, level=level)  # type: ignore

        return logger

    @staticmethod
    def _sink(message: Message) -> None:
        simplified = LoggingUtils._formatter(message.record)
        print(json.dumps(simplified), file=sys.stderr)

    @staticmethod
    def _formatter(record: Dict[str, Any]) -> Dict[str, Any]:
        log_record = {
            "level": record["level"].name,
            "line": record["line"],
            "file": record["file"].name,
            "message": record["message"],
            "time": record["time"].isoformat(),
        }
        log_record.update(record["extra"])

        if record.get("exception"):
            log_record["exception"] = list(
                # chain.from_iterable flattens list of lists
                itertools.chain.from_iterable(
                    e.split("\n")
                    for e in LoggingUtils.exception_formatter.format_exception(
                        *record["exception"]
                    )
                    if e
                )
            )

        return log_record
