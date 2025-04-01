import logging
import os
from aiohttp import web
from aiogram import types
from bot import dp, on_startup, on_shutdown

logging.basicConfig(level=logging.INFO)

async def handle_root(request):
    return web.Response(text="Bot is alive!")

async def handle_webhook(request):
    try:
        data = await request.json()
        update = types.Update.to_object(data)
        await dp.process_update(update)
        return web.Response(status=200, text="OK")
    except Exception as e:
        logging.error("Ошибка обработки запроса от Telegram", exc_info=e)
        return web.Response(status=500, text="Internal Server Error")

async def start():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_post("/", handle_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    from bot import bot
    webhook_url = "https://kibronik-bot.onrender.com"
    await bot.set_webhook(webhook_url)
    logging.info(f"Webhook установлен: {webhook_url}")
    logging.info("Bot is running via webhook on Render...")

    await on_startup(dp)

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    import asyncio
    asyncio.run(start())