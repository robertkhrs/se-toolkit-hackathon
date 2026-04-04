from openai import AsyncOpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1" 
)

def get_system_prompt(language: str) -> str:
    return f"""
    Speak natural, modern, and conversational {language}. Avoid overly formal, clunky, or robotic phrasing.
    You are a language tutor for roleplay. We are playing a scenario: 'Ordering food in a restaurant'. You are the waiter.
    Respond in {language}. If the user makes a mistake, correct it.
    Also, extract 1-2 useful words from your reply or the user's prompt to help them learn.
    ALWAYS reply in valid JSON format with three keys:
    "reply": "your response",
    "correction": "analysis of mistakes or empty string",
    "new_words": [{{"word": "foreign word", "translation": "russian translation"}}]
    """

async def get_agent_response(user_text: str, language: str) -> dict:
    response = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": get_system_prompt(language)}, # <--- Передаем язык сюда
            {"role": "user", "content": user_text}
        ]
    )
    result = response.choices[0].message.content
    return json.loads(result)