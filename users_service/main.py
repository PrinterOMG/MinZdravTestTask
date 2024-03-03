from fastapi import FastAPI

from api.routers import router as main_router
from utils.logger_middleware import LoggerMiddleware

app = FastAPI(docs_url='/api/docs', redoc_url='/api/redoc', openapi_url='/api/openapi.json')

app.include_router(main_router, prefix='/api/v1')

app.add_middleware(LoggerMiddleware)
