from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import smtplib
from email.mime.text import MIMEText
import os

TOKEN = "7713823915:AAHSvUOlvYtCoszYItEE3-pZNKjGackKw9Q"
ORGANIZERS_EMAIL = "kserandr@gmail.com"
EMAIL_PASSWORD = "your_email_password"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("ℹ Информация о маршруте"))
keyboard.add(KeyboardButton("📍 Отправить местоположение", request_location=True))
keyboard.add(KeyboardButton("🚨 Срочная помощь"))

# Функция отправки письма организаторам
def send_email(subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = ORGANIZERS_EMAIL
        msg["To"] = ORGANIZERS_EMAIL
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(ORGANIZERS_EMAIL, EMAIL_PASSWORD)
        server.sendmail(ORGANIZERS_EMAIL, ORGANIZERS_EMAIL, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот-помощник для туристов на БУТ. Выберите действие:", reply_markup=keyboard)

# Информация о маршруте
@dp.message_handler(lambda message: message.text == "ℹ Информация о маршруте")
async def send_info(message: types.Message):
    info_text = "Большая Уральская Тропа – это уникальный маршрут, соединяющий лучшие природные достопримечательности Урала..."
    await message.answer(info_text)

# Отправка местоположения
@dp.message_handler(content_types=['location'])
async def location_handler(message: types.Message):
    if message.location:
        lat, lon = message.location.latitude, message.location.longitude
        email_message = f"Турист отправил местоположение: {lat}, {lon}"
        send_email("Местоположение туриста", email_message)
        await message.answer("Ваше местоположение отправлено организаторам.")

# Экстренная помощь
@dp.message_handler(lambda message: message.text == "🚨 Срочная помощь")
async def emergency_handler(message: types.Message):
    send_email("Срочная помощь", f"Турист {message.from_user.full_name} ({message.from_user.id}) запрашивает помощь!")
    await message.answer("Сообщение отправлено организаторам! Они свяжутся с вами как можно скорее.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
