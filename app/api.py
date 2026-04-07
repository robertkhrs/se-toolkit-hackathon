from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from database import init_db, async_session, Message, Vocabulary
from agent import get_agent_response
from sqlalchemy import select
import os

app = FastAPI()

@app.get("/")
async def root():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "index.html")
    return FileResponse(file_path)

class ChatRequest(BaseModel):
    user_id: int
    text: str
    language: str = "Italian"
    topic: str = "Ordering food in a restaurant"

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    agent_data = await get_agent_response(req.text, req.language, req.topic)
    
    async with async_session() as session:
        # Сохраняем сообщения (как раньше)
        user_msg = Message(user_id=req.user_id, role="user", content=req.text)
        bot_msg = Message(user_id=req.user_id, role="assistant", content=agent_data["reply"])
        session.add_all([user_msg, bot_msg])
        
        # Сохраняем новые слова в словарь!
        if "new_words" in agent_data:
            for word_item in agent_data["new_words"]:
                new_vocab = Vocabulary(
                    user_id=req.user_id, 
                    language=req.language, 
                    word=word_item["word"], 
                    translation=word_item["translation"]
                )
                session.add(new_vocab)
                
        await session.commit()
        
    return {"status": "ok", "reply": agent_data["reply"], "correction": agent_data["correction"]}

@app.get("/quiz/{user_id}")
async def get_quiz(user_id: int):
    async with async_session() as session:
        stmt = select(Vocabulary).where(Vocabulary.user_id == user_id)
        result = await session.execute(stmt)
        words = result.scalars().all()

        if not words:
            return {"words": []}

        return {"words": [{"word": w.word, "translation": w.translation} for w in words]}