import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = logging.INFO


def set_uvicorn_logger():
    uvicorn_loggers = ["uvicorn", "uvicorn.access", "uvicorn.error"]
    for logger_name in uvicorn_loggers:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers.clear()
        if not uvicorn_logger.hasHandlers():
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
            uvicorn_logger.addHandler(handler)
            uvicorn_logger.setLevel(logging.INFO)
