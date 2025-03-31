from flask import Flask
from threading import Thread
from bot import start_bot

app = Flask(__name__)

@app.route('/')
def index():
    return "Kibronik Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    Thread(target=start_bot).start()