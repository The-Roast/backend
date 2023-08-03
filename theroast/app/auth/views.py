from fastapi import APIRouter

from theroast.app.auth.endpoints import auth

auth_router = APIRouter()
auth_router.include_router(auth.router, prefix="/auth", tags=["auth"])