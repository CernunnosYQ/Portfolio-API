from fastapi import APIRouter

from routes.v1 import user, blogpost, auth

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(user.router, prefix="", tags=["users"])
v1_router.include_router(blogpost.router, prefix="", tags=["blogpost"])
v1_router.include_router(auth.router, prefix="", tags=["auth"])
