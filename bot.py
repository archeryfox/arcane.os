import os
import asyncio
import random
import re
from collections import defaultdict
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import aiohttp

from app.utils.logger import setup_logger, format_ai_response

load_dotenv()

logger = setup_logger("arcana_os")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/free"
FREE_MODELS = [
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-2-9b-it:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
]

# === ИГРОВЫЕ ПРАВИЛА (system prompt) ===
SYSTEM_PROMPT = """Ты — Мастер ARCANA.OS, текстовый RPG-бот в Telegram.

МИР: Фэнтези-сеттинг с магией, монстрами и подземельями.
ПЕРСОНАЖ ИГРОКА: У игрока есть характеристики (Сила, Ловкость, Интеллект, Харизма), HP, мана, инвентарь, золото.
ЗАКЛИНАНИЯ: НЕТ ПРЕДЕФИНИРОВАННОГО СПИСКА. Игрок придумывает любое название. Ты генерируешь эффект, урон, стоимость маны на лету.

ПРАВИЛА:
1. Отвечай в ролевом стиле, 2-4 предложения. На русском!
2. Используй стандартный Markdown для форматирования:
   **жирный**, *курсив*, `код`, [ссылка](url), - список, > цитата.
3. Никаких Telegram-специфичных тегов (tg-spoiler, и т.д.).
4. Начисляй XP и лут за победы. Генерируй сам броски и их результаты
5. Не ломай четвёртую стену — ты внутри мира.
6. Если игрок пытается что-то невозможное — опиши последствия в игровом контексте. Коротко, предложи какие возможные действия
7. Игрок использует сокращения: c-cast t-target m-material(m=Xn+Xn, где n-мощность)
8. Кастуй без персонажа, дай дефолтные значения
9. Любое заклинание работает — придумывай эффект, урон (NdN+M), ману (10-50), тип.
"""

# === ИСТОРИЯ РАЗГОВОРОВ ===
# Per-user conversation history: {user_id: [{"role": "user"/"assistant", "content": "..."}]}
MAX_HISTORY = 20  # last N messages to keep in context
conversations: dict[int, list[dict[str, str]]] = defaultdict(list)

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in environment variables")

# MarkdownV2 special chars that need escaping
MDV2_ESCAPE = re.compile(r"([_*\[\]()~`>#+\-=|{}.!])")


def escape_mdv2(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    return MDV2_ESCAPE.sub(r"\\\1", text)


bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
dp = Dispatcher()


async def ask_openrouter(text: str, user_id: int) -> str:
    """Send message to OpenRouter with conversation history."""
    history = conversations[user_id]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": text},
        ],
        "temperature": 0.7,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, headers=headers, json=payload) as resp:
            if resp.status != 200:
                error_text = await resp.text()
                logger.error(f"OpenRouter error {resp.status}: {error_text}")
                return "Ошибка при обращении к OpenRouter API"
            data = await resp.json()
            response = data["choices"][0]["message"]["content"]

    # Update history
    history.append({"role": "user", "content": text})
    history.append({"role": "assistant", "content": response})
    # Trim to last N messages
    if len(history) > MAX_HISTORY:
        conversations[user_id] = history[-MAX_HISTORY:]

    return response


def roll_dice(notation: str) -> int:
    """Parse dice notation like '2d6+3' and return result."""
    import re
    match = re.match(r"(\d*)d(\d+)([+-]\d+)?", notation.replace(" ", ""))
    if not match:
        return 0
    count = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    return sum(random.randint(1, sides) for _ in range(count)) + modifier


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "Привет! Я ARCANA.OS бот.\n\n"
        "Команды:\n"
        "/cast `название заклинания` — наколдовать что угодно (нет ограничений)\n"
        "/reset — сбросить историю разговора\n"
        "Или просто напиши сообщение — отвечу через OpenRouter."
    )
    await message.answer(escape_mdv2(text))


@dp.message(Command("reset"))
async def cmd_reset(message: types.Message):
    user_id = message.from_user.id
    if user_id in conversations:
        del conversations[user_id]
    await message.answer("История разговора сброшена.", parse_mode=None)


@dp.message(Command("cast"))
async def cmd_cast(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(escape_mdv2("Укажи заклинание: /cast огненный шар"))
        return

    spell_name = args[1].strip()
    user_text = f"Кастую заклинание: {spell_name}. Опиши эффект, урон, стоимость маны."

    try:
        response = await ask_openrouter(user_text, message.from_user.id)
        formatted = format_ai_response(response)
        await message.answer(formatted, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.exception("Error handling cast")
        await message.answer("Ошибка при касте заклинания", parse_mode=None)


@dp.message(F.text)
async def handle_message(message: types.Message):
    user_text = message.text
    logger.info(f"Received message from {message.from_user.id}: {user_text}")

    try:
        response = await ask_openrouter(user_text, message.from_user.id)
        formatted = format_ai_response(response)
        await message.answer(formatted, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.exception("Error handling message")
        await message.answer("Произошла ошибка при обработке сообщения", parse_mode=None)


async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())