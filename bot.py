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

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот канала Kibronik.")

@dp.callback_query_handler(lambda c: c.data == "publish")
async def publish_post(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    post_data = post_drafts.get(user_id)

    if not post_data:
        await callback_query.answer("Черновик не найден", show_alert=True)
        return

    post_text = post_data["text"]
    image_path = post_data["image_path"]

    try:
        with open(image_path, "rb") as image:
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=image,
                caption=post_text,
                #parse_mode=ParseMode.MARKDOWN
                parse_mode=ParseMode.HTML
            )
        await callback_query.message.delete()
        await bot.send_message(chat_id=user_id, text="✅ Пост опубликован в канал!")
    except Exception as e:
        logging.error("Ошибка публикации: %s", e)
        await bot.send_message(user_id, f"Ошибка при публикации: {e}")

async def on_startup(dispatcher):
    logging.info("Бот запущен.")

async def on_shutdown(dispatcher):
    logging.warning("Бот остановлен.")
    await bot.session.close()
