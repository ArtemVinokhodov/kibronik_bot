from flask import Flask
from bot import start_bot
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Kibronik Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    # ❗ Вызываем без потока, просто запускаем как основной процесс
    start_bot()
