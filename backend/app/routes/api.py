from fastapi import APIRouter

from .endpoints import task, auth

router = APIRouter()

router.include_router(task.router, prefix="/tasks", tags=["tasks"])
router.include_router(auth.router, prefix="/login", tags=["login"])
