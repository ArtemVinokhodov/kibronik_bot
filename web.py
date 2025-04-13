import logging
import os
import json

from aiohttp import web
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from bot import dp, on_startup, on_shutdown, post_drafts
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO)

async def create_post(request):
    logging.info("💡 POST /create_post triggered")
    try:
        body = await request.text()
        logging.info(f"🔍 Request body: {body}")

        data = json.loads(body)
        post_text = data.get("text")
        image_path = data.get("image_path", "images/my_image.png")
        image_data = data.get("image_data")

        # Сохраняем картинку в файл до проверки
        if image_data:
            try:
                with open(image_path, "wb") as f:
                    f.write(bytes(image_data))
                logging.info("🖼️ Картинка сохранена в images/my_image.png")
            except Exception as e:
                logging.error(f"❌ Ошибка при сохранении изображения: {e}")

        if not post_text or not os.path.isfile(image_path):
            logging.error("❌ Отсутствует текст или изображение")
            return web.json_response({"error": "Не передан текст или изображение"}, status=400)

        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("Опубликовать", callback_data="publish")
        )

        try:
            with open(image_path, "rb") as image:
                await bot.send_photo(
                    chat_id=OWNER_ID,
                    photo=image,
                    caption=post_text,
                    parse_mode=types.ParseMode.MARKDOWN,
                    reply_markup=markup
                )
            logging.info("✅ Пост успешно отправлен в Telegram")
        except Exception as telegram_error:
            logging.error(f"⚠️ Ошибка отправки сообщения в Telegram: {telegram_error}")
            return web.json_response({"error": str(telegram_error)}, status=500)

        post_drafts[OWNER_ID] = {
            "text": post_text,
            "image_path": image_path
        }

        return web.json_response({"status": "ok"}, status=200)

    except Exception as e:
        logging.error(f"🔥 Ошибка обработки запроса в create_post: {e}")
        return web.json_response({"error": str(e)}, status=500)

async def handle_root(request):
    return web.Response(text="Bot is alive!")

async def handle_webhook(request):
    try:
        data = await request.json()
        update = types.Update.to_object(data)
        await dp.process_update(update)
        return web.Response(status=200, text="OK")
    except Exception as e:
        logging.error("❗ Ошибка обработки запроса от Telegram", exc_info=e)
        return web.Response(status=500, text="Internal Server Error")

async def start():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_post("/", handle_webhook)

    app.router.add_post("/create_post", create_post)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    webhook_url = "https://kibronik-bot.onrender.com"
    await bot.set_webhook(webhook_url)
    logging.info(f"🔗 Webhook установлен: {webhook_url}")
    logging.info("🚀 Bot is running via webhook on Render...")

    await on_startup(dp)

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import asyncio
    asyncio.run(start())
