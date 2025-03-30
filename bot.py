from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import openai
import os
import datetime

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

async def generate_news():
    now = datetime.datetime.utcnow().strftime("%d %B %Y")
    prompt = f"Generate a short, tech-style Telegram news post about the latest updates in AI, crypto, or tech. Format it like a post for a Telegram channel with a title, 2-3 short paragraphs, and a tone similar to @exploitex. Add a news source link as markdown inside the text. Date: {now}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message['content']
    return content

@dp.message_handler(commands=['draft'])
async def send_draft(message: types.Message):
    if str(message.from_user.id) != os.getenv("OWNER_ID"):
        await message.reply("⛔ Доступ запрещён")
        return

    await message.answer("✍️ Генерирую пост...")
    news = await generate_news()
    await message.answer(news, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
