import logging
import asyncio
from aiohttp import web
from bot import dp, bot, on_startup, on_shutdown

WEBHOOK_HOST = 'https://kibronik-bot.onrender.com'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 10000

async def handle_webhook(request):
    # Получаем update и передаём диспетчеру
    update = await request.json()
    await dp.process_update(dp.bot.update_class(**update))
    return web.Response()

async def handle_root(request):
    return web.Response(text="✅ Bot is alive!")

async def on_startup_webhook(app):
    await on_startup(dp)
    await bot.set_webhook(WEBHOOK_URL)
    print("📡 Webhook установлен:", WEBHOOK_URL)

async def on_shutdown_webhook(app):
    await bot.delete_webhook()
    await on_shutdown(dp)
    print("🛑 Webhook удалён")

async def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.router.add_get("/", handle_root)

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

