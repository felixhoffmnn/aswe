import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

LOG_LEVEL = os.getenv("LOGURU_LEVEL", "TRACE")

if LOG_LEVEL in ["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]:
    logger.remove()
    logger.add(sys.stderr, level=LOG_LEVEL)
