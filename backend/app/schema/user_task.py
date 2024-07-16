from typing import Optional

from pydantic import BaseModel, field_serializer
from datetime import datetime

from app.schema.base import BaseResponse


class UserTask(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: Optional[str] = None
    brief: Optional[str] = None
    content: Optional[str] = None
    deadline: Optional[datetime] = None
    parent_id: Optional[int] = None
    is_completed: bool = False

    @field_serializer("deadline")
    def serialize_dt(self, deadline: datetime, _info):
        if deadline is None:
            return None
        return datetime.strftime(deadline, "%Y-%m-%d")


class BaseQueryRequest(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: Optional[str] = None
    brief: Optional[str] = None
    content: Optional[str] = None
    deadline: Optional[datetime] = None
    parent_id: Optional[int] = None
    is_completed: bool = False


class CreateTaskRequest(BaseQueryRequest):
    user_id: int
    title: str
    content: str


class CompleteTaskRequest(BaseQueryRequest):
    is_completed: bool = True


class PageResponse(BaseResponse):
    data: dict
    page: int = 1
    per_page: int = 10
