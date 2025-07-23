import os

import openai
from fastapi import HTTPException

from services.firestore_service import get_history, save_message

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


async def get_openai_response(user_message: str) -> str:
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_message}]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def event_generator(session_id: str):
    history = get_history(session_id)

    # Construct OpenAI-compatible message list
    messages = [{"role": msg["role"], "content": msg["message"]} for msg in history]

    try:
        response = await get_openai_response(messages)
        full_reply = ""
        async for chunk in response:
            if "choices" in chunk:
                delta = chunk["choices"][0]["delta"].get("content", "")
                full_reply += delta
                yield f"data: {delta}\n\n"

        # Save final assistant reply
        save_message(session_id, "assistant", full_reply)

    except Exception as e:
        yield f"data: [Error] {str(e)}\n\n"
