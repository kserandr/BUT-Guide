import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from flask import Flask, request
import threading

TOKEN = "7713823915:AAHSvUOlvYtCoszYItEE3-pZNKjGackKw9Q"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Создаем Flask-приложение для поддержки работы на Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

@bot.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Привет! Я твой бот-гид по Большой Уральской Тропе. Чем могу помочь?")

@bot.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply("Я могу помочь тебе с информацией о Большой Уральской Тропе. Задавай вопросы!")

@bot.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text.lower()
    
    if "маршрут" in user_text:
        await message.reply("На БУТ есть несколько маршрутов. Какой именно вас интересует?")
    elif "погода" in user_text:
        await message.reply("Для информации о погоде используйте сайт: gismeteo.ru")
    elif "помощь" in user_text:
        await message.reply("Если вам нужна помощь, напишите, в чем именно проблема.")
    else:
        await message.reply("Я вас не понял. Попробуйте задать другой вопрос.")

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start_polling())

if __name__ == "__main__":
    # Запуск веб-сервера Flask в отдельном потоке
    threading.Thread(target=start_bot).start()
    
    app = Flask(__name__)
    
    @app.route("/")
    def home():
        return "Bot is running"
    
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
