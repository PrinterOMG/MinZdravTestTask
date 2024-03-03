from fastapi import FastAPI

from api.routers import router as main_router

app = FastAPI()

app.include_router(main_router, prefix='/api/v1')
