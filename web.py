from flask import Flask
from bot import start_bot, send_initial_draft_async
import asyncio
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Kibronik Bot is running!"

def run_flask():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(send_initial_draft_async())
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    start_bot()
