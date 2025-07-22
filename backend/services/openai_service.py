import os

import openai
from fastapi import HTTPException

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
