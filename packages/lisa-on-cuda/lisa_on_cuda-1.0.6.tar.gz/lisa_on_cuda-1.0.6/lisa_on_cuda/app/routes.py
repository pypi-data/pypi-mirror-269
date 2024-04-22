import json
import logging
from fastapi import APIRouter

from ..utils import session_logger


router = APIRouter()


@router.get("/health")
@session_logger.set_uuid_logging
def health() -> str:
    try:
        logging.info("health check")
        return json.dumps({"msg": "ok"})
    except Exception as e:
        logging.error(f"exception:{e}.")
        return json.dumps({"msg": "request failed"})
