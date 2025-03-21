import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Dictionary to store subscribed users
subscribed_users = set()

# Function to handle /start command
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    subscribed_users.add(chat_id)
    await update.message.reply_text("Welcome! You will receive daily football betting tips at 3:58 AM.")

# Function to handle /subscribe command
async def subscribe(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    subscribed_users.add(chat_id)
    await update.message.reply_text("You have subscribed to daily betting tips!")

# Function to handle /tips command
async def tips(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await send_betting_tips(chat_id)

# Function to send betting tips
async def send_betting_tips(chat_id):
    message = (
        "🔥 **Today's Football Betting Tips** 🔥\n"
        "✅ Over 2.5 Goals\n"
        "✅ BTTS (Both Teams to Score)\n"
        "✅ Correct Score: 2-1\n"
        "✅ High-probability bets: 70%+ win probability"
    )
    await app.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

# Function to send daily tips to all subscribed users at 3:58 AM
async def send_daily_tips():
    for chat_id in subscribed_users:
        await send_betting_tips(chat_id)

# Initialize the bot using ApplicationBuilder
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("subscribe", subscribe))
app.add_handler(CommandHandler("tips", tips))

# Set up the scheduler for daily tips at 3:58 AM
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: asyncio.run(send_daily_tips()), 'cron', hour=3, minute=58)
scheduler.start()

# Start the bot
print("Bot is running...")
app.run_polling()
