import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils.executor import start_webhook
import os

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

initial_post = '''🧠 5 бесплатных AI-инструментов для поиска стартапов:

1. **Trends.co** — показывает растущие тренды и идеи.
2. **Glasp** — подборки статей и видео по трендам.
3. **There's an AI for That** — каталог всех AI-сервисов.
4. **Hacker News Trends** — отслеживает популярные темы HN.
5. **IdeaBuddy** — помогает превратить идею в бизнес.

Подробности и ссылки — в первом комментарии.'''

post_drafts = {}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот канала Kibronik.")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

@dp.callback_query_handler(lambda c: c.data == "publish")
async def publish_post(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id="@kibronik", text=post_drafts.get(callback_query.from_user.id, ""), parse_mode=ParseMode.MARKDOWN)
    await callback_query.message.edit_text("✅ Опубликовано!")

async def on_startup(dispatcher):
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Опубликовать", callback_data="publish")
    )
    await bot.send_message(OWNER_ID, initial_post, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    post_drafts[int(OWNER_ID)] = initial_post

async def on_shutdown(dispatcher):
    logging.warning("Shutting down..")

WEBHOOK_PATH = ''
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 10000

def start_bot():
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )