from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот канала Kibronik.")

@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.answer("Ты написал: " + message.text)

if __name__ == "__main__":
    executor.start_polling(dp)
