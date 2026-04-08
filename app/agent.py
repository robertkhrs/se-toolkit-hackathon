from openai import AsyncOpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1" 
)

def get_system_prompt(language: str, topic: str) -> str:
    return f"""
You are a language tutor for roleplay. Scenario: '{topic}'.
Target language: {language}.

RULES:
1. Respond in character in the target language.
2. If the user makes a spelling, grammar, or vocabulary mistake, you MUST point out the exact wrong word and provide the correct spelling/grammar in your "correction" field.
3. The "new_words" array is a MISTAKE TRACKER — it has ONLY one purpose:
   - Add a word to "new_words" IF AND ONLY IF the user made a spelling, grammar, or lexical mistake in this message.
   - The "word" field must contain the CORRECTED version of the word in the target language.
   - The "translation" field must contain a brief explanation/translation in Russian (1-2 words).
   - If the user's message is completely correct, "new_words" MUST be an empty list [].
   - NEVER add random conversational words, NEVER add words the user spelled correctly.

JSON FORMAT:
{{
  "reply": "your in-character response",
  "correction": "You wrote 'X', but the correct spelling is 'Y'. [Brief explanation]",
  "new_words": [{{"word": "correct_word", "translation": "краткий перевод на русском"}}]
}}

EXAMPLE OF CORRECTION:
If user types: "Я хочу соус смитану"
Your correction MUST be: "Вы написали 'смитану', но правильно писать 'сметану' (сметана)."
Your new_words should include: {{"word": "сметана", "translation": "сметана"}}
"""

async def get_agent_response(user_text: str, language: str, topic: str = "Ordering food in a restaurant", history: list = None) -> dict:
    messages = [
        {"role": "system", "content": get_system_prompt(language, topic)},
    ]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_text})

    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={ "type": "json_object" },
        messages=messages
    )
    result = response.choices[0].message.content
    return json.loads(result)