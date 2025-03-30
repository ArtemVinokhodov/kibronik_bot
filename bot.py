from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils import executor
import os
import openai
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
OWNER_ID = os.getenv("OWNER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

post_drafts = {}

initial_post = """⚙️ 5 бесплатных AI-инструментов, которые реально экономят время:

1. [**Perplexity**](https://www.perplexity.ai/) — умный поисковик с ответами на основе ИИ  
2. [**Remove.bg**](https://www.remove.bg/) — мгновенно удаляет фон с фото  
3. [**Tome**](https://tome.app/) — презентации и лендинги на основе текста  
4. [**Gamma**](https://gamma.app/) — альтернатива PowerPoint на базе GPT  
5. [**Scribble Diffusion**](https://scribblediffusion.com/) — превращает наброски в изображения

—
Подписывайся на [@kibronik](https://t.me/kibronik) — только полезные AI-инструменты и свежие техно-новости.
"""

async def send_initial_draft_async():
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Опубликовать", callback_data="publish")
    )
    await asyncio.sleep(3)
    await bot.send_message(OWNER_ID, initial_post, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    post_drafts[OWNER_ID] = initial_post

def send_initial_draft():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_initial_draft_async())

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
