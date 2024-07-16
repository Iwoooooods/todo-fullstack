from typing import List

from fastapi import APIRouter, Depends, status
from redis.asyncio import Redis

from app.schema.user_task import CreateTaskRequest, CompleteTaskRequest, BaseQueryRequest, UserTask
from app.service.user_task_service import get_task_service, TaskService
from app.database.redis_base import get_client

router = APIRouter()


@router.get("/in_process/{user_id}", response_model=List[UserTask], status_code=status.HTTP_200_OK)
async def in_process_tasks(user_id: int, task_service: TaskService = Depends(get_task_service)):
    return await task_service.completed_or_in_process(user_id, True)


@router.get("/completed_or_overdue/{user_id}", response_model=List[UserTask], status_code=status.HTTP_200_OK)
async def completed_or_overdue_tasks(user_id: int,
                                     task_service: TaskService = Depends(get_task_service)):
    return await task_service.completed_or_in_process(user_id, False)


@router.post("/create_task", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_task(req: CreateTaskRequest, task_service: TaskService = Depends(get_task_service),
                      redis_client: Redis = Depends(get_client)):
    return await task_service.create_task(req, redis_client)


@router.put("/task_done")
async def complete_task(task_id: int, user_id, req: CompleteTaskRequest,
                        task_service: TaskService = Depends(get_task_service),
                        redis_client: Redis = Depends(get_client)):
    return await task_service.update_task(task_id, user_id, req, redis_client)


@router.put("/task_update")
async def update_task(task_id: int, user_id: int, req: BaseQueryRequest,
                      task_service: TaskService = Depends(get_task_service),
                      redis_client: Redis = Depends(get_client)):
    return await task_service.update_task(task_id, user_id, req, redis_client)


@router.delete("/delete_task")
async def delete_task(task_id: int, user_id: int, task_service: TaskService = Depends(get_task_service),
                      redis_client=Depends(get_client)):
    return await task_service.delete_task(task_id, user_id, redis_client)


@router.get("/warning/{user_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def warning_message(user_id: int, task_service: TaskService = Depends(get_task_service),
                          redis_client=Depends(get_client)):
    return await task_service.overdue_warning(user_id, redis_client)
