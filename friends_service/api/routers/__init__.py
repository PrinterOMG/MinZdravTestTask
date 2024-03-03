from fastapi import APIRouter

from .friends import router as friends_router


router = APIRouter()

router.include_router(friends_router)
