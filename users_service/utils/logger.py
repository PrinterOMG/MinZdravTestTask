import json
import logging
from datetime import datetime
from logging import Formatter


class JsonFormatter(Formatter):
    def __init__(self):
        super(JsonFormatter, self).__init__()

    def format(self, record: logging.LogRecord, *args, **kwargs):
        time = datetime.fromtimestamp(record.created).astimezone().replace(microsecond=0).isoformat()

        json_log = {
            'message': record.getMessage(),
            'time': time
        }

        if hasattr(record, 'request'):
            json_log['request'] = record.request

        if hasattr(record, 'response'):
            json_log['response'] = record.response

        duration = record.duration if hasattr(record, 'duration') else record.msecs
        json_log['duration'] = duration

        return json.dumps(json_log)


logger = logging.root

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger.handlers = [handler]
logger.setLevel(logging.DEBUG)
