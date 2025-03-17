import os
import asyncio
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# File to store subscribed users
SUBSCRIBERS_FILE = "subscribers.txt"

# Load subscribed users from file
def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r") as file:
            return set(json.load(file))
    return set()

# Save subscribed users to file
def save_subscribers():
    with open(SUBSCRIBERS_FILE, "w") as file:
        json.dump(list(subscribed_users), file)

# Dictionary to store subscribed users
subscribed_users = load_subscribers()

# Function to handle /start command
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    subscribed_users.add(chat_id)
    save_subscribers()
    await update.message.reply_text("Welcome! You have been subscribed to daily football betting tips at 3:47 AM.")

# Function to handle /subscribe command
async def subscribe(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in subscribed_users:
        subscribed_users.add(chat_id)
        save_subscribers()
        await update.message.reply_text("You have subscribed to daily betting tips!")
    else:
        await update.message.reply_text("You're already subscribed.")

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

# Function to send daily tips to all subscribed users at 3:47 AM
async def send_daily_tips():
    if subscribed_users:
        print(f"Sending daily tips to {len(subscribed_users)} users...")
        for chat_id in subscribed_users:
            asyncio.create_task(send_betting_tips(chat_id))
    else:
        print("No subscribers to send tips to.")

# Initialize the bot using ApplicationBuilder
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("subscribe", subscribe))
app.add_handler(CommandHandler("tips", tips))

# Set up the scheduler for daily tips at 3:47 AM
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: asyncio.create_task(send_daily_tips()), 'cron', hour=3, minute=47)
scheduler.start()

# Start the bot
print("Bot is running...")
app.run_polling()
