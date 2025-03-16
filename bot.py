import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Set TELEGRAM_BOT_TOKEN in environment variables.")

# Initialize the bot
app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! I will send you football betting tips daily.")

async def tips(update: Update, context: CallbackContext):
    await update.message.reply_text("Here are today's football tips:\n✅ Over 2.5 Goals\n✅ BTTS\n✅ Correct Score: 2-1")

# Define commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tips", tips))

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
