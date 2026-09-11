import os
import asyncio
import logging
import random
import re
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import aiohttp

load_dotenv()

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
[debug unlimited spell mode]
ПРАВИЛА:
1. Отвечай в ролевом стиле, 2-4 предложения. На русском!
2. Используй ТОЛЬКО Telegram MarkdownV2 форматирование:
   *жирный* — одинарные звёздочки
   _курсив_ — нижние подчёркивания
   `код` — обратные кавычки
   ~зачёркнуто~ — тильды
   ||спойлер|| — двойные вертикальные черты
   [ссылка](url) — ссылки
   НЕ используй **жирный**, ## заголовки, - списки — это сломанный формат.
3. Экранируй спецсимволы: _ * [ ] ( ) ~ ` > # + - = | { } . !
   Пример: "Привет\\!" а не "Привет!"
4. Начисляй XP и лут за победы. Генерируй сам броски и их результаты
5. Не ломай четвёртую стену — ты внутри мира.
6. Если игрок пытается что-то невозможное — опиши последствия в игровом контексте. Коротко, предложи кракто возможные действия
7. Игрок использует сокращения: c-cast t-target m-material(m=Xn+Xn, где n-мощность)
8. Кастуй без персонажа, дай дефолтные значения
"""

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in environment variables")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MarkdownV2 special chars that need escaping
MDV2_ESCAPE = re.compile(r"([_*\[\]()~`>#+\-=|{}.!])")


def escape_mdv2(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    return MDV2_ESCAPE.sub(r"\\\1", text)


bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
dp = Dispatcher()

SPELLS = {
    "огненный шар": {
        "name": "🔥 Огненный шар",
        "damage": "2d6+3",
        "description": "Шар пламени взрывается у цели, нанося урон огнём.",
        "mana_cost": 15,
    },
    "магическая стрела": {
        "name": "✨ Магическая стрела",
        "damage": "1d4+1",
        "description": "Непромахивающаяся стрела чистой магии.",
        "mana_cost": 5,
    },
    "исцеление": {
        "name": "💚 Исцеление",
        "damage": "2d4+2 HP",
        "description": "Заживляет раны цели.",
        "mana_cost": 10,
    },
    "щит": {
        "name": "🛡 Щит веры",
        "damage": "+2 КД",
        "description": "Невидимый барьер защищает от атак на 1 раунд.",
        "mana_cost": 8,
    },
}


async def ask_openrouter(text: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
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
            return data["choices"][0]["message"]["content"]


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
        "/cast `заклинание` - наколдовать (огненный шар, магическая стрела, исцеление, щит)\n"
        "/spells - список заклинаний\n"
        "Или просто напиши сообщение - отвечу через OpenRouter."
    )
    await message.answer(escape_mdv2(text))


@dp.message(Command("spells"))
async def cmd_spells(message: types.Message):
    lines = ["📜 *Доступные заклинания:*\n"]
    for key, spell in SPELLS.items():
        name = escape_mdv2(spell['name'])
        mana = escape_mdv2(str(spell['mana_cost']))
        desc = escape_mdv2(spell['description'])
        dmg = escape_mdv2(spell['damage'])
        lines.append(f"*{name}* - {mana} маны")
        lines.append(f"  {desc} (урон/эффект: {dmg})")
        lines.append("")
    await message.answer("\n".join(lines))


@dp.message(Command("cast"))
async def cmd_cast(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(escape_mdv2("Укажи заклинание: /cast огненный шар"))
        return

    spell_key = args[1].lower().strip()
    spell = SPELLS.get(spell_key)

    if not spell:
        await message.answer(escape_mdv2(f"Неизвестное заклинание: {spell_key}\nСписок: /spells"))
        return

    result = roll_dice(spell["damage"].split()[0]) if "d" in spell["damage"] else spell["damage"]
    effect = f"{result}" if isinstance(result, int) else result

    response = (
        f"{spell['name']} ✨\n"
        f"💙 Мана: -{spell['mana_cost']}\n"
        f"🎯 Эффект: {effect}\n"
        f"_{spell['description']}_"
    )
    await message.answer(escape_mdv2(response))


@dp.message(F.text)
async def handle_message(message: types.Message):
    user_text = message.text
    logger.info(f"Received message from {message.from_user.id}: {user_text}")

    try:
        response = await ask_openrouter(user_text)
        await message.answer(response)
    except Exception as e:
        logger.exception("Error handling message")
        await message.answer("Произошла ошибка при обработке сообщения")


async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
