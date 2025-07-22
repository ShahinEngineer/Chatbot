from pydantic import BaseModel


class MessageData(BaseModel):
    session_id: str = "test_session"
    role: str = "user"
    message: str = "Hello from API!"


class ChatRequest(BaseModel):
    session_id: str
    message: str
