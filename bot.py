import os
import telegram
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler

# Get the bot token from Railway environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize the bot
bot = telegram.Bot(token=BOT_TOKEN)

# Dictionary to store subscribed users
subscribed_users = set()

def start(update, context):
    """Handles the /start command"""
    update.message.reply_text(
        "Welcome! Use /subscribe to receive daily betting tips automatically."
    )

def subscribe(update, context):
    """Handles the /subscribe command"""
    chat_id = update.message.chat_id
    if chat_id not in subscribed_users:
        subscribed_users.add(chat_id)
        update.message.reply_text("✅ You have subscribed to daily betting tips at 8 AM!")
    else:
        update.message.reply_text("ℹ️ You are already subscribed.")

def tips(update, context):
    """Handles the /tips command"""
    chat_id = update.message.chat_id
    send_betting_tips(chat_id)

def send_betting_tips(chat_id):
    """Sends betting tips"""
    message = (
        "🔥 **Today's Football Betting Tips** 🔥\n"
        "✅ Over 2.5 Goals\n"
        "✅ BTTS (Both Teams to Score)\n"
        "✅ Correct Score: 2-1\n"
        "✅ High-probability bets: 70%+ win probability"
    )
    bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

def send_daily_tips():
    """Sends tips to all subscribed users daily at 8 AM"""
    for chat_id in subscribed_users:
        send_betting_tips(chat_id)

# Set up the bot
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

# Define commands
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("subscribe", subscribe))
dp.add_handler(CommandHandler("tips", tips))

# Schedule daily tips at 8 AM
scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_tips, 'cron', hour=8, minute=0)
scheduler.start()

# Start the bot
updater.start_polling()
updater.idle()
