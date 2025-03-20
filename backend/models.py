from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    target_website = Column(String, nullable=False)
    search_keyword = Column(String, nullable=False)
    loop = Column(Integer, default=1)
    status = Column(String, default="pending")  # pending, running, completed, failed
    ordering = Column(Integer, default=0)
    date_add = Column(DateTime(timezone=True), server_default=func.now()) 