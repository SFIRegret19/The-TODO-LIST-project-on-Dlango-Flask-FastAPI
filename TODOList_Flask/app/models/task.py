from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, Text, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enums.task_priority import Priority

class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    priority = Column(Enum (Priority, default=Priority.NOT_URGENT_NOT_IMPORTANT))
    is_completed = Column(Boolean, default=False)
    category = Column(String(50), default='Все')
    progress = Column(Integer, default=0)
    attachment = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    due_date = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    completed_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)
    
    user = relationship("User", back_populates="tasks")

    # проверка категории на Заглавную букву
    @property
    def formatted_category(self):
        return self.category.capitalize() if self.category else self.category
    
    @property
    def priority_str(self):
        return str(self.priority).replace("_", " ").title() # Преобразует Enum в строку

    # Автоматически ставим дату завершения
    def mark_completed(self):
        self.is_completed = True
        self.completed_at = datetime.now(timezone.utc)