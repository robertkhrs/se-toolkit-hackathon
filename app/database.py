from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Text, BigInteger
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"), echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    role: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)

class Vocabulary(Base):
    __tablename__ = 'vocabulary'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    language: Mapped[str] = mapped_column(Text)
    word: Mapped[str] = mapped_column(Text)
    translation: Mapped[str] = mapped_column(Text)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)