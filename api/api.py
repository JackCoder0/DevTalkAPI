from fastapi import APIRouter
from api.endpoints import auth, lessons

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])
