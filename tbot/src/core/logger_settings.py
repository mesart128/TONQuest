import logging.config

import yaml
from colorlog import ColoredFormatter
from pythonjsonlogger import jsonlogger

from src.core.config import LOG_DIR, PROJECT_DIR, REQ_ID_CONTEXT


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        log_record["context_id"] = REQ_ID_CONTEXT.get()


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # We set request id, so we can use it in the formatter to show it in the log records.
        # Also, this fields will be added to the graylog extra fields and will be searchable.
        context_id = REQ_ID_CONTEXT.get()

        if context_id:
            record.context_id = context_id
            record.short_context_id = context_id[:3] + "..." + context_id[-3:]
        else:
            record.context_id = ""
            record.short_context_id = ""

        # setattr(record, "api_source", settings.GRAYLOG_API_SOURCE)

        return super().format(record)


class CustomColoredFormatter(ColoredFormatter, CustomFormatter):
    pass


def setup_logging():
    settings_module = "DEV"
    if settings_module == "DEV":
        file_name = PROJECT_DIR / "logging.yml"
    elif settings_module == "PROD":
        file_name = PROJECT_DIR / "logging.prod.yml"
    else:
        raise ValueError(f"Unknown settings module: {settings_module}")

    with open(file_name) as log_file:
        content = log_file.read()

    # graylog_host, graylog_port = settings.GRAYLOG_BIND.split(":") if settings.GRAYLOG_BIND
    # else None
    graylog_host, graylog_port = "localhost", "12201"
    log_config = content.format(
        logdir=LOG_DIR, graylog_host=graylog_host, graylog_port=graylog_port
    )
    logging.config.dictConfig(yaml.safe_load(log_config))
