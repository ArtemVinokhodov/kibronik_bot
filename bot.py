from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils import executor
import os
import openai
import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
OWNER_ID = os.getenv("OWNER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

post_drafts = {}

# Генерация свежей новости
async def generate_news():
    now = datetime.datetime.utcnow().strftime("%d %B %Y")
    prompt = f"Generate a short Telegram post (2-3 paragraphs) with the latest AI, crypto or tech news for {now}. Add a source link inside the text using markdown."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

@dp.message_handler(commands=['draft'])
async def send_draft(message: types.Message):
    if str(message.from_user.id) != OWNER_ID:
        await message.reply("⛔ Доступ запрещён")
        return
    await message.answer("✍️ Генерирую пост...")
    news = await generate_news()

    post_drafts[message.from_user.id] = news

    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Опубликовать", callback_data="publish")
    )
    await message.answer(news, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'publish')
async def publish_post(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if str(user_id) != OWNER_ID:
        await callback_query.answer("⛔ Не авторизован", show_alert=True)
        return
    post = post_drafts.get(user_id)
    if not post:
        await callback_query.answer("Пост не найден", show_alert=True)
        return

    await bot.send_message(CHANNEL_ID, post, parse_mode=ParseMode.MARKDOWN)
    await callback_query.answer("✅ Пост опубликован в канал!")
    del post_drafts[user_id]

def start_bot():
    executor.start_polling(dp)

if __name__ == "__main__":
    start_bot()
