from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    email_id    = Column(Integer, ForeignKey("emails.id"), nullable=True)
    title       = Column(String(500))
    deadline    = Column(String(255), nullable=True)
    priority    = Column(String(50), default="normal")
    status      = Column(String(50), default="pending")
    created_at  = Column(DateTime, default=func.now())