import sys
import logging
from loguru import logger

# print(logging.Logger.manager.loggerDict)
# {'concurrent.futures': <Logger concurrent.futures (WARNING)>, 'concurrent': <logging.PlaceHolder object at 0x0000014C2F967208>, 'asyncio': <Logger asyncio (WARNING)>, 'uvicorn.error': <Logger uvicorn.error (WARNING)>, 'uvicorn': <logging.PlaceHolder object at 0x0000014C300A2708>, 'fastapi': <Logger fastapi (WARNING)>}

def _init_loggers():
    logging.getLogger('uvicorn').disabled = True
    logging.getLogger('fastapi').disabled = True
    logging.getLogger('uvicorn.error').disabled = True

    logger.remove()
    logger.add(sys.stdout, colorize=True, diagnose=False, format="<g>{time:YYYY-MM-DD HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u>{name}</u></c> : {message}")

_init_loggers()