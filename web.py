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

async def handle(request):
    return web.Response(text="Bot is live!")

async def on_startup_webhook(app):
    await on_startup(dp)
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown_webhook(app):
    await bot.delete_webhook()
    await on_shutdown(dp)

def setup_routes(app):
    app.router.add_post(WEBHOOK_PATH, lambda request: dp.webhook_handler(request))
    app.router.add_get("/", handle)

async def main():
    app = web.Application()
    setup_routes(app)
    app.on_startup.append(on_startup_webhook)
    app.on_shutdown.append(on_shutdown_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBAPP_HOST, WEBAPP_PORT)
    await site.start()

    print("✅ Bot is running via webhook on Render...")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
