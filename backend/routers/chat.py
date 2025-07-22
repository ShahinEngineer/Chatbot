from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from models.message_model import ChatRequest
from services.firestore_service import save_message
from services.openai_service import event_generator

router = APIRouter()


@router.post("/")
async def chat(data: ChatRequest):
    session_id = data.session_id
    save_message(session_id, "user", data.message)
    return {"session_id": session_id, "response": "accepted"}


@router.get("/sse")
async def chat_sse(session_id: str = Query(...)):
    return StreamingResponse(event_generator(session_id), media_type="text/event-stream")
