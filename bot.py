import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import os

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)
Bot.set_current(bot)  # Фикс для контекста
dp = Dispatcher(bot)

post_drafts = {}

def generate_post():
    return """🧠 5 бесплатных AI-инструментов для поиска стартапов:

1. [Trends.co](https://trends.co) — показывает растущие тренды и идеи.  
2. [Glasp](https://glasp.co) — подборки статей и видео по трендам.  
3. [There’s an AI for That](https://theresanaiforthat.com) — каталог всех AI-сервисов.  
4. [Hacker News Trends](https://hntrends.com) — отслеживает популярные темы HN.  
5. [IdeaBuddy](https://ideabuddy.com) — помогает превратить идею в бизнес.

Подписывайся на [@kibronik](https://t.me/kibronik) — чтобы не пропустить новые инструменты."""

preview_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/512px-ChatGPT_logo.svg.png"

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот канала Kibronik.")

@dp.callback_query_handler(lambda c: c.data == "publish")
async def publish_post(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    post = post_drafts.get(user_id)
    if not post:
        await callback_query.answer("❌ Черновик не найден", show_alert=True)
        return
    try:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=preview_image, caption=post, parse_mode=ParseMode.MARKDOWN)
        await callback_query.message.edit_text("✅ Пост опубликован в канал!")
    except Exception as e:
        print("Ошибка:", e)

async def on_startup(dispatcher):
    print("📨 Бот запущен, отправка первого черновика...")
    post = generate_post()
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Опубликовать", callback_data="publish")
    )
    await bot.send_photo(chat_id=OWNER_ID, photo=preview_image, caption=post, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    post_drafts[OWNER_ID] = post

async def on_shutdown(dispatcher):
    logging.warning("Shutting down...")
    await bot.session.close()
