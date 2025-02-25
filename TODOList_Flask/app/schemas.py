from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enums.task_priority import Priority  # Импортируем Enum для приоритета


# Схема для создания задачи
class CreateTask(BaseModel):
    title: str
    content: str | None = None  # Поле не обязательное
    priority: Priority = Priority.NOT_URGENT_NOT_IMPORTANT  # Используем Enum
    category: str = 'Все'  # Значение по умолчанию
    progress: int = 0
    attachment: str | None = None
    due_date: datetime | None = None  # Тип даты
    slug: str | None = None  # Уникальный идентификатор

    class Config:
        use_enum_values = True  # Для того, чтобы Pydantic использовал значения enum при сериализации


# Схема для обновления задачи
class UpdateTask(BaseModel):
    title: str | None = None
    content: str | None = None
    is_completed: bool | None = None  # Статус завершения задачи
    priority: Priority | None = None  # Используем Enum для приоритета
    category: str | None = None
    progress: int | None = None
    attachment: str | None = None
    due_date: datetime | None = None  # Тип даты
    slug: str | None = None  # Можно обновить slug

    class Config:
        use_enum_values = True  # Для использования значений enum при сериализации

# Схема для отображения задачи (например, для чтения данных)
class TaskOut(BaseModel):
    id: int
    title: str
    content: str | None
    priority: Priority
    category: str
    progress: int
    attachment: str | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    due_date: datetime | None
    slug: str

    class Config:
        use_enum_values = True  # Для использования значений enum при сериализации

# Схема для создания пользователя
class CreateUser(BaseModel):
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    age: int = Field(ge=100, gt=0)  # Указываем, что возраст должен быть больше 0, меньше 100
    password: str
    slug: str | None = None  # Уникальный идентификатор


# Схема для отображения пользователя
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    age: int
    full_name: str
    created_at: datetime
    updated_at: datetime
    slug: str

    class Config:
        orm_mode = True  # Позволяет использовать SQLAlchemy-объекты


# Схема для входа пользователя
class LoginUser(BaseModel):
    email: EmailStr
    password: str