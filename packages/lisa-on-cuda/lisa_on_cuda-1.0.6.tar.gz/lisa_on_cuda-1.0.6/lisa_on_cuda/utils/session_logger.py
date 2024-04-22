import contextvars
import logging
from functools import wraps
from typing import Callable

logging_uuid = contextvars.ContextVar("uuid")
formatter = '%(asctime)s | %(uuid)s [%(pathname)s:%(module)s %(lineno)d] %(levelname)s | %(message)s'


loggingType = logging.CRITICAL | logging.ERROR | logging.WARNING | logging.INFO | logging.DEBUG


def change_logging(level_log: loggingType = logging.INFO) -> None:
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.uuid = logging_uuid.get("uuid")
        if isinstance(record.msg, str):
            record.msg = record.msg.replace("\\", "\\\\").replace("\n", "\\n")
        return record

    logging.setLogRecordFactory(record_factory)
    logging.basicConfig(level=level_log, format=formatter, force=True)


def set_uuid_logging(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        import uuid

        current_uuid = f"{uuid.uuid4()}"
        logging_uuid.set(current_uuid)
        return func(*args, **kwargs)

    return wrapper
