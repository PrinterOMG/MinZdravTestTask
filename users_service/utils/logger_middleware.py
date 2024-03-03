import math
import time

from starlette.middleware.base import BaseHTTPMiddleware

from utils.logger import logger


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = math.ceil((time.time() - start_time) * 1000)

        response_headers = dict(response.headers.items())
        requests_headers = dict(request.headers.items())

        message = (
            f'{request.method} Request for {str(request.url)} took {duration} ms. Status code: {response.status_code}'
        )

        logger.info(
            message,
            extra={
                'duration': duration,
                'request': {
                    'method': request.method,
                    'headers': requests_headers,
                    'size': int(requests_headers.get('content-length', 0)),
                    'url': str(request.url)
                },
                'response': {
                    'status_code': response.status_code,
                    'size': int(response_headers.get('content-length', 0)),
                    'headers': response_headers
                }
            }
        )

        return response
