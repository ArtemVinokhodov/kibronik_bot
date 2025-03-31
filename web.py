import logging
import asyncio
from aiohttp import web
from aiogram.utils.executor import start_webhook
from bot import dp, on_startup, on_shutdown

WEBHOOK_PATH = ''
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 10000

async def handle(request):
    return web.Response(text="Bot is live!")

async def start():
    app = web.Application()
    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBAPP_HOST, WEBAPP_PORT)
    await site.start()

    print("🚀 Starting aiogram webhook...")
    await start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())
