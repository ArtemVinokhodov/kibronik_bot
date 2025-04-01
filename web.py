import logging
import os
from aiohttp import web
from aiogram import types
from bot import dp, bot, on_startup, on_shutdown

WEBHOOK_HOST = 'https://kibronik-bot.onrender.com'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

async def handle_root(request):
    return web.Response(text="✅ Bot is alive!")

async def handle_webhook(request):
    try:
        data = await request.json()
        update = types.Update.to_object(data)
        await dp.process_update(update)
    except Exception as e:
        logging.error("Ошибка обработки запроса от Telegram", exc_info=e)
    return web.Response()

async def on_startup_webhook(app):
    await on_startup(dp)
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"📡 Webhook установлен: {WEBHOOK_URL}")
    logging.info("✅ Bot is running via webhook on Render...")

async def on_shutdown_webhook(app):
    await bot.delete_webhook()
    await on_shutdown(dp)

async def start():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    app.on_startup.append(on_startup_webhook)
    app.on_shutdown.append(on_shutdown_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import asyncio
    asyncio.run(start())
