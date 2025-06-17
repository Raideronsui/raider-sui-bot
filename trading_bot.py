import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import asyncio
from sui_trader import execute_trade_logic

# Load .env
load_dotenv()

# Environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("~V Raider Bot Activated!")

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await execute_trade_logic()
    await update.message.reply_text(f"Trade Result: {result}")

# Scheduled trade wrapper
def run_scheduled_trade():
    asyncio.run(execute_trade_logic())

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trade", trade))

    # Scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scheduled_trade, trigger="interval", hours=6)
    scheduler.start()

    logger.info("Bot running...")
    app.run_polling()

if __name__ == '__main__':
    main()

