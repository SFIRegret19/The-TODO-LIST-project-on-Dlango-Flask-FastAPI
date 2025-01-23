from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, Text,String, Boolean, DateTime
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__='tasks'
    __table_args__={'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    priority = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    category = Column(String(50), default='Все')
    progress = Column(Integer, default=0)
    attachment = Column(String(255))
    created_at = Column(DateTime)
    due_date = Column(DateTime)
    updated_at = Column(DateTime)
    completed_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)
    
    user = relationship("User", back_populates="tasks")