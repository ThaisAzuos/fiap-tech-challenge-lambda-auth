import logging
import json
import uuid
import os

class StructuredLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, level, message, correlation_id=None, **kwargs):
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        log_entry = {
            'timestamp': None,  # Will be added by CloudWatch
            'level': level,
            'message': message,
            'correlation_id': correlation_id,
            'service': 'fiap-tech-challenge-lambda-auth',
            'version': os.environ.get('VERSION', '1.0.0'),
            **kwargs
        }

        if level == 'INFO':
            self.logger.info(json.dumps(log_entry))
        elif level == 'ERROR':
            self.logger.error(json.dumps(log_entry))
        elif level == 'WARNING':
            self.logger.warning(json.dumps(log_entry))
        else:
            self.logger.debug(json.dumps(log_entry))

# Global logger instance
logger = StructuredLogger()
