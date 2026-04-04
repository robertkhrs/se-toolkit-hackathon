import asyncio
import os
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher()


class LanguageForm(StatesGroup):
    waiting_for_language = State()

API_URL = "http://api:8000/chat"

user_languages = {}

# Persistent reply keyboard
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎭 Start/Reset"),
            KeyboardButton(text="🌐 Change Language"),
        ],
        [KeyboardButton(text="🧠 Quiz")],
    ],
    resize_keyboard=True,
    persistent=True,
    input_field_placeholder="Choose an action...",
)

# Helper to detect if text matches a keyboard button
def get_button_action(text: str) -> str | None:
    button_map = {
        "🎭 Start/Reset": "start_reset",
        "🌐 Change Language": "change_language",
        "🧠 Quiz": "quiz",
    }
    return button_map.get(text.strip())


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_languages.pop(message.from_user.id, None)
    welcome_text = (
        "👋 Welcome! I'm your language learning assistant.\n\n"
        "I'll help you practice conversations, correct your mistakes, "
        "and build a personalized vocabulary quiz.\n\n"
        "Just chat with me in any language, and I'll keep track of "
        "new words for you. Use the buttons below to get started!"
    )
    await message.answer(welcome_text, reply_markup=main_keyboard)


@dp.message(Command("language"))
async def lang_cmd(message: types.Message):
    args = message.text.split()
    if len(args) > 1:
        new_lang = args[1]
        user_languages[message.from_user.id] = new_lang
        await message.answer(
            f"✅ Language changed to **{new_lang}**. What would you like to chat about?",
            parse_mode="Markdown",
            reply_markup=main_keyboard,
        )
    else:
        await message.answer(
            "⚠️ Please specify a language after the command, for example: `/language Spanish`",
            parse_mode="Markdown",
            reply_markup=main_keyboard,
        )


@dp.message(Command("quiz"))
async def quiz_cmd(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                f"http://api:8000/quiz/{message.from_user.id}"
            )
            data = response.json()

            if not data["words"]:
                await message.answer(
                    "📚 Your vocabulary is still empty! Start chatting with me "
                    "and I'll collect new words for you to review later.",
                    reply_markup=main_keyboard,
                )
                return

            quiz_text = "🧠 **Your vocabulary review:**\n\n"
            for w in data["words"]:
                quiz_text += f"🔹 **{w['word']}** — {w['translation']}\n"

            quiz_text += "\nTry writing a sentence using one of these words!"
            await message.answer(
                quiz_text, parse_mode="Markdown", reply_markup=main_keyboard
            )

        except Exception:
            await message.answer(
                "❌ Sorry, I couldn't load your vocabulary. Please try again later.",
                reply_markup=main_keyboard,
            )


@dp.message(LanguageForm.waiting_for_language)
async def process_language_change(message: types.Message, state: FSMContext):
    new_lang = message.text.strip()
    user_languages[message.from_user.id] = new_lang
    await message.answer(
        f"✅ Language changed to **{new_lang}**. What would you like to chat about?",
        parse_mode="Markdown",
        reply_markup=main_keyboard,
    )
    await state.clear()


@dp.message()
async def handle_message(message: types.Message, state: FSMContext):
    # Skip if the user is in the middle of a state machine flow
    current_state = await state.get_state()
    if current_state is not None:
        return

    # Check if the user pressed a keyboard button
    action = get_button_action(message.text)

    if action == "start_reset":
        await start_cmd(message)
        return

    if action == "change_language":
        await message.answer(
            "🌐 Please type the name of the language you'd like to practice "
            "(e.g., *Spanish*, *French*, *German*), and I'll switch to it right away!",
            parse_mode="Markdown",
            reply_markup=main_keyboard,
        )
        await state.set_state(LanguageForm.waiting_for_language)
        return

    if action == "quiz":
        await quiz_cmd(message)
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    current_lang = user_languages.get(message.from_user.id, "Italian")

    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "user_id": message.from_user.id,
                "text": message.text,
                "language": current_lang,
            }
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            answer_text = f"🗣 {data['reply']}"
            if data["correction"]:
                answer_text += f"\n\n🛠 **Correction:** {data['correction']}"

            await message.answer(
                answer_text, parse_mode="Markdown", reply_markup=main_keyboard
            )

        except httpx.HTTPError:
            await message.answer(
                "🔌 I'm having trouble reaching the backend server. "
                "Please try again in a moment.",
                reply_markup=main_keyboard,
            )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())