import asyncio
from aiogram import executor
from bot import dp, on_startup

async def start():
    from aiohttp import web
    app = web.Application()
    # Просто для проверки: пусть root отдает OK
    app.router.add_get("/", lambda request: web.Response(text="Bot is live!"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    await on_startup(dp)
    # Не polling! Мы запускаем webhook (косвенно)
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start())
