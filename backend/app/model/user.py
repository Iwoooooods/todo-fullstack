from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary,func
from sqlalchemy.orm import as_declarative, class_mapper


@as_declarative()
class Base:
    def to_dict(self) -> dict:
        """
        :return:
        """
        return {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)
    disabled = Column(Boolean, default=False)
