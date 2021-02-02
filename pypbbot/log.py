import sys
import logging
from loguru import logger

def _init_loggers():
    logger.remove()
    logger.add(sys.stdout, colorize=True, diagnose=False, format="<g>{time:YYYY-MM-DD HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u><{name}></u></c>: {message}")

_init_loggers()

class LoguruHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "default": {
            "class": "pypbbot.log.LoguruHandler",
        },
    },
    "loggers": {
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO"
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
        },
    },
}