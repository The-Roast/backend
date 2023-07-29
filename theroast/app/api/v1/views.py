from fastapi import APIRouter

from theroast.app.api.v1.endpoints import user, digest, newsletter

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(digest.router, prefix="/digest", tags=["digest"])
api_router.include_router(newsletter.router, prefix="/newsletter", tags=["newsletter"])