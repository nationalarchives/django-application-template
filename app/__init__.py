import logging

from django.conf import settings

logging.basicConfig(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)
