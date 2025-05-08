import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import openai
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные из .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройка клиентов
openai.api_key = OPENAI_API_KEY
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

# FastAPI-приложение (если ты используешь webhook или бота через FastAPI)
app = FastAPI()

# Telegram App
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Пример команды start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой Telegram-бот с OpenAI.")

# Пример обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

# Регистрация обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск (если напрямую через Python, не через FastAPI)
if __name__ == "__main__":
    application.run_polling()