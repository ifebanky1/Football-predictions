import os
import telegram
from telegram.ext import Updater, CommandHandler

# Get the bot token from Railway environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize the bot
bot = telegram.Bot(token=BOT_TOKEN)

def start(update, context):
    update.message.reply_text("Welcome! I will send you football betting tips daily.")

def tips(update, context):
    update.message.reply_text("Here are today's football tips:\n✅ Over 2.5 Goals\n✅ BTTS\n✅ Correct Score: 2-1")

# Set up the bot
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

# Define commands
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("tips", tips))

# Start the bot
updater.start_polling()
updater.idle(
worker: python bot.py
python-telegram-bot
requests
pip freeze > requirements.txt
BOT_TOKEN=your_telegram_bot_token
