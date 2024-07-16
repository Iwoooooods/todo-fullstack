from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import Depends, HTTPException
from loguru import logger
from sqlalchemy import text, select, and_, or_, func, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import database_client
from app.model.task import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize the task repository
        :param db:
        """
        self.db = db

    async def get_task_by_user(self, user_id: int) -> Any:
        """
        Get all tasks
        :param user_id:
        :return:
        """
        try:
            results = await self.db.execute(select(Task).filter(Task.user_id == user_id))
            tasks = results.scalars().all()
            if not tasks:
                raise HTTPException(status_code=404, detail="Task not found")
            return tasks
        except SQLAlchemyError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def query_tasks(self, user_id: int, order_by: Optional[str] = None, asc: bool = False,
                          due_before: Optional[datetime] = None, lte: bool = False, **filters) -> Any:

        query = select(Task).filter(Task.user_id == user_id)

        for key, value in filters.items():
            query = query.filter(getattr(Task, key) == value)

        if due_before:
            if lte:
                query.filter(getattr(Task, "deadline") <= due_before)
            else:
                query.filter(getattr(Task, "deadline") > due_before)

        if order_by:
            if asc:
                query = query.order_by(text(f"{order_by} asc"))
            else:
                query = query.order_by(text(f"{order_by} desc"))

        try:
            result = await self.db.execute(query)
            tasks = result.scalars().all()
            return tasks
        except SQLAlchemyError as e:
            raise e

    async def get_in_process_task(self, user_id: int, in_process: bool = True) -> Any:
        query = select(Task)
        if in_process:
            query = query.where(
                and_(Task.is_completed == False,
                     # Task.user_id == user_id,
                     or_(
                         Task.deadline == None,
                         Task.deadline >= func.current_date()
                     )
                     )
            ).order_by(desc(Task.created_at))
        else:
            query = query.where(
                and_(Task.user_id == user_id),
                or_(Task.is_completed == True,
                    Task.deadline < func.current_date())
            ).order_by(desc(Task.updated_at))

        try:
            logger.info(f"{__name__}:{query}")
            print(datetime.today())
            result = await self.db.execute(query)
            tasks = result.scalars().all()
            return tasks
        except SQLAlchemyError as error:
            raise error

    async def get_task_by_id(self, id: int) -> Any:
        try:
            result = await self.db.execute(select(Task).filter(Task.id == id))
            task: Task = result.scalars().first()
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return task
        except SQLAlchemyError as e:
            raise e

    async def add_task(self, task: Task) -> Optional[Task]:
        try:
            self.db.add(task)
            await self.db.commit()
            await self.db.refresh(task)
            return task
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def update_task(self, task_id: int, update_fields: Dict[str, Any]) -> None:
        result = await self.db.execute(select(Task).filter(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        for key, value in update_fields.items():
            if hasattr(task, key) and value:
                setattr(task, key, value)
        try:
            await self.db.commit()
            logger.success("Update Successfully!")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(str(e))
            raise e

    async def delete_task(self, task_id: int) -> None:
        try:
            result = await self.db.execute(select(Task).where(Task.id == task_id))
            task = result.scalars().first()
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            await self.db.delete(task)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e


async def get_repository(db: AsyncSession = Depends(database_client.get_db)) -> TaskRepository:
    """
    Get the task repository
    :param db:
    :return:
    """
    return TaskRepository(db)
