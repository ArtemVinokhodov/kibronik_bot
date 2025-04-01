import logging
import os
import asyncio
from aiohttp import web
from bot import dp, bot, on_startup, on_shutdown

WEBHOOK_HOST = 'https://kibronik-bot.onrender.com'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 10000

# ✅ Обрабатываем POST / — Telegram будет сюда слать обновления
async def handle_webhook(request):
    return await dp.webhook_handler(request)

# 👋 Просто проверка, что сервер жив
async def handle_root(request):
    return web.Response(text="✅ Bot is alive!")

async def on_startup_webhook(app):
    await on_startup(dp)
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"📡 Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown_webhook(app):
    await bot.delete_webhook()
    await on_shutdown(dp)

async def main():
    logging.basicConfig(level=logging.INFO)
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_post("/", handle_webhook)  # 👈 ВАЖНО!

    app.on_startup.append(on_startup_webhook)
    app.on_shutdown.append(on_shutdown_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBAPP_HOST, WEBAPP_PORT)
    await site.start()

    logging.info("✅ Bot is running via webhook on Render...")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
