from backend.db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from flask_login import UserMixin

class User(UserMixin, Base):  # Наследуем от UserMixin
    __tablename__ = 'users'
    __table_args__ = {'keep_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    slug = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates="user")

    @property
    def full_name(self):
        """Возвращает полное имя пользователя."""
        return f"{self.firstname} {self.lastname}"

    def get_id(self):
        """Метод, который возвращает уникальный идентификатор пользователя для Flask-Login."""
        return str(self.id)