import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Set TELEGRAM_BOT_TOKEN in environment variables.")

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! I will send you football betting tips daily.")

def tips(update: Update, context: CallbackContext):
    update.message.reply_text("Here are today's football tips:\n✅ Over 2.5 Goals\n✅ BTTS\n✅ Correct Score: 2-1")

# Set up the bot
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

# Define commands
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("tips", tips))

# Start the bot
updater.start_polling()
updater.idle()
