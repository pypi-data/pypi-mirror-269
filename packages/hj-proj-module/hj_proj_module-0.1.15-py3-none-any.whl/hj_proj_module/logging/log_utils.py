import os
from datetime import datetime
import threading
import logging.config
from pythonjsonlogger import jsonlogger


def get_json_formatter(prefix: str):
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        # override
        def add_fields(self, log_record, record, message_dict):
            super().add_fields(log_record, record, message_dict)
            log_record["datetime"] = datetime.utcnow().isoformat()
            log_record["level"] = record.levelname
            log_record["logger_name"] = record.name
            log_record["message"] = f"{prefix}{record.getMessage()}"
            log_record["process"] = os.getpid()
            log_record["thread"] = threading.current_thread().name
            log_record["filename"] = record.filename
            log_record["line_number"] = record.lineno

    return CustomJsonFormatter


def set_logging_config(
    prefix: str = "", json_log: bool = False, log_level: str = "INFO"
):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": get_json_formatter(prefix=prefix),
                    "format": "%(severity)s %(asctime)s %(name)s %(funcName)s %(pathname)s %(lineno)s %(message)s",
                },
                "detail": {
                    "format": "{asctime} {process} {processName} {name} [{levelname}] {message}",
                    "style": "{",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json" if json_log else "detail",
                },
            },
            "loggers": {
                "": {"handlers": ["console"], "level": log_level},
            },
        }
    )
