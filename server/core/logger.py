import asyncio
import logging.config
import os
import typing

import yaml
from aiogram import Bot

from core.config import base_config
# from gunicorn import glogging
# from gunicorn import glogging
from pythonjsonlogger import jsonlogger

from core.config import BASE_DIR, CONTEXT_ID, LOG_DIR, LoggerSettings
from core.enums import CustomLoggingLevels

bot = Bot(token=base_config.bot_token)


class TelegramLogger:

    def __init__(self):
        self.bot = Bot(token=base_config.bot_token)

    async def info(self, text: str = "Default", chat_ids: typing.List[int] = base_config.admin_ids_list):
        for chat_id in chat_ids:
            await self.bot.send_message(chat_id=chat_id, text=text)

def setup_telegram_logger():
    logger = TelegramLogger()
    return logger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        log_record["context_id"] = CONTEXT_ID.get()


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # We set request id, so we can use it in the formatter to show it in the log records.
        # Also, this fields will be added to the graylog extra fields and will be searchable.
        context_id = CONTEXT_ID.get()
        pathname = record.pathname
        shortened_path = os.path.join(
            os.path.basename(os.path.dirname(pathname)), os.path.basename(pathname)
        )
        record.shortened_path = shortened_path
        if context_id:
            record.context_id = context_id
            record.short_context_id = context_id[:3] + "..." + context_id[-3:]
        else:
            record.context_id = ""
            record.short_context_id = ""

        # setattr(record, "api_source", settings.GRAYLOG_API_SOURCE)

        return super().format(record)


def setup_logging(
    logger_settings: typing.Optional[LoggerSettings] = None,
    log_dir: str = str(LOG_DIR).replace("\\", "/"),
):
    if logger_settings is None:
        logger_settings = LoggerSettings()
    settings_module = logger_settings.settings_module
    if settings_module == "DEV":
        file_name = BASE_DIR / "logging.dev.yml"
    elif settings_module == "PROD":
        file_name = BASE_DIR / "logging.prod.yml"
    else:
        raise ValueError(f"Unknown settings module: {settings_module}")
    logging.info(f"Using logging config from {file_name}")
    with open(file_name) as log_file:
        content = log_file.read()

    log_config = content.format(
        logdir=log_dir,
        graylog_host=logger_settings.graylog_host,
        graylog_port=logger_settings.graylog_port,
    )
    logging.config.dictConfig(yaml.safe_load(log_config))

    # Set custom levels
    for level in CustomLoggingLevels:
        logging.addLevelName(level.value, level.name)


# class GunicornLogger(glogging.Logger):
#     def setup(self, cfg):
#         setup_logging(logger_settings=LoggerSettings())
