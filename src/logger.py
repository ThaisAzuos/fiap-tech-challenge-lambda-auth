import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def log_event(event):
    logger.info(json.dumps(event))
