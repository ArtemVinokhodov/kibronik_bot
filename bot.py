import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

Bot.set_current(bot)

post_drafts = {}

preview_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/512px-ChatGPT_logo.svg.png"

def generate_post():
    return """5 бесплатных AI-инструментов для поиска стартапов:

1. [Trends.co](https://trends.co) - показывает растущие тренды и идеи.  
2. [Glasp](https://glasp.co) - подборки статей и видео по трендам.  
3. [There’s an AI for That](https://theresanaiforthat.com) - каталог всех AI-сервисов.  
4. [Hacker News Trends](https://hntrends.com) - отслеживает популярные темы HN.  
5. [IdeaBuddy](https://ideabuddy.com) - помогает превратить идею в бизнес.

Подписывайся на [@kibronik](https://t.me/kibronik) - чтобы не пропустить новые инструменты.
"""

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот канала Kibronik.")

@dp.callback_query_handler(lambda c: c.data == "publish")
async def publish_post(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    post = post_drafts.get(user_id)
    if not post:
        await callback_query.answer("Черновик не найден", show_alert=True)
        return
    try:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=preview_image, caption=post, parse_mode=ParseMode.MARKDOWN)
        await callback_query.message.delete()
        await bot.send_message(chat_id=user_id, text="✅ Пост опубликован в канал!")

    except Exception as e:
        logging.error("Ошибка публикации: %s", e)
        await bot.send_message(user_id, f"Ошибка при публикации: {e}")

async def on_startup(dispatcher):
    logging.info("Бот запущен, отправка первого черновика...")
    post = generate_post()
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Опубликовать", callback_data="publish")
    )
    await bot.send_photo(chat_id=OWNER_ID, photo=preview_image, caption=post, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    post_drafts[OWNER_ID] = post

async def on_shutdown(dispatcher):
    logging.warning("Бот остановлен.")
    await bot.session.close()