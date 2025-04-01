import logging
import asyncio
from aiohttp import web
from bot import dp, bot, on_startup, on_shutdown

async def handle_root(request):
    return web.Response(text="✅ Bot is alive!")

async def start():
    app = web.Application()
    app.router.add_get("/", handle_root)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    logging.info("📨 Бот запущен, отправка первого черновика...")
    await on_startup(dp)
    logging.info("📡 Webhook установлен: https://kibronik-bot.onrender.com/")
    logging.info("✅ Bot is running via webhook on Render...")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await on_shutdown(dp)
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())
