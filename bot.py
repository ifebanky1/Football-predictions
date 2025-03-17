import os
import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Get the bot token from Railway environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# File to store subscribed users
USER_DATA_FILE = "subscribed_users.json"

# Load subscribed users from JSON file
def load_subscribed_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return set(json.load(file))
    return set()

# Save subscribed users to JSON file
def save_subscribed_users():
    with open(USER_DATA_FILE, "w") as file:
        json.dump(list(subscribed_users), file)

# Initialize subscribed users
subscribed_users = load_subscribed_users()

# Function to handle /start command
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    subscribed_users.add(chat_id)
    save_subscribed_users()
    await update.message.reply_text("Welcome! You will receive daily football betting tips at 3:25 AM.")

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

# Function to send daily tips to all subscribed users at 3:25 AM
async def send_daily_tips():
    for chat_id in subscribed_users:
        try:
            await send_betting_tips(chat_id)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

# Initialize the bot using ApplicationBuilder
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tips", tips))

# Set up the scheduler for daily tips at 3:25 AM
scheduler = AsyncIOScheduler()
scheduler.add_job(send_daily_tips, "cron", hour=3, minute=25)
scheduler.start()

# Start the bot
print("Bot is running...")
app.run_polling()
