import os

from config.util import strtobool

from .features import *  # noqa: F401, F403
from .production import *  # noqa: F401, F403

DEBUG: bool = strtobool(os.getenv("DEBUG", "False"))
