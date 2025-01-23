from pydantic import BaseModel, Field

class CreateTask(BaseModel):
    title: str
    content: str
    priority: int
    category: str
    progress: int
    due_date: str
    attachment: str | None = None

class UpdateTask(BaseModel):
    title: str | None = None
    content: str | None = None
    priority: int | None = None
    category: str | None = None
    progress: int | None = None
    due_date: str | None = None
    attachment: str | None = None