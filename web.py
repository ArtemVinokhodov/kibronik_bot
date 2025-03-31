import asyncio
from aiohttp import web
from bot import dp, on_startup

async def handle_root(request):
    return web.Response(text="✅ Bot is alive!")

async def start():
    app = web.Application()
    app.router.add_get("/", handle_root)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    print("📨 Бот запущен, отправка первого черновика...")
    await on_startup(dp)
    print("✅ Bot is running via webhook on Render...")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start())

