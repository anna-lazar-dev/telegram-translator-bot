import logging
from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()
logger = logging.getLogger(__name__)

@router.errors()
async def on_error(event: ErrorEvent):
    logger.exception("Unhandled error", exc_info=event.exception)
