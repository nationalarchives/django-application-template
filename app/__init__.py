import logging

from django.conf import settings

logging.basicConfig(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)
logger.debug("DEBUG")
logger.info("INFO")
logger.warning("WARNING")
logger.error("ERROR")
logger.critical("CRITICAL")
