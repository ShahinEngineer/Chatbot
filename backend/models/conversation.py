from typing import List, Optional

class Message(BaseModel):
    sender: str
    content: str
    timestamp: str

class Conversation(BaseModel):
    id: str
    messages: List[Message]
    created_at: str
    updated_at: Optional[str] = None