from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, class_mapper
from sqlalchemy.sql import func


@as_declarative()
class Base:
    def to_dict(self) -> dict:
        """
        :return:
        """
        return {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}


class Task(Base):
    __tablename__ = 'tasks'

    id: int = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=True)
    updated_at = Column(DateTime, default=None, onupdate=func.current_timestamp(), nullable=True)
    title = Column(String(255), nullable=False)
    brief = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=True)
    deadline = Column(DateTime, nullable=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    parent_id = Column(BigInteger, nullable=True)
