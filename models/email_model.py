from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database.db import Base

class Email(Base):
    __tablename__ = "emails"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    gmail_id    = Column(String(255), unique=True, nullable=False)   # Gmail's own message ID
    sender      = Column(String(255))
    subject     = Column(String(500))
    snippet     = Column(Text)
    body        = Column(Text)
    date        = Column(String(100))
    category    = Column(String(50), default="uncategorized")
    fetched_at  = Column(DateTime, default=func.now())