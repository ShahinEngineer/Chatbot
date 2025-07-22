from fastapi import APIRouter
from models.message_model import ChatRequest
from services.firestore_service import get_history, save_message
from services.openai_service import get_openai_response

router = APIRouter()


@router.post("/")
async def chat(data: ChatRequest):
    session_id = data.session_id
    user_msg = {"role": "user", "content": data.message}

    history = get_history(session_id)
    history.append(user_msg)

    ai_response = await get_openai_response(history)

    save_message(session_id, "user", data.message)
    save_message(session_id, "assistant", ai_response)

    return {"session_id": session_id, "response": ai_response}
