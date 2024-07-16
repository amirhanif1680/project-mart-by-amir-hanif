from sqlmodel import SQLModel, Field
from typing import Optional

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    email: str
    created_at: Optional[str] = None
