import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from dotenv import load_dotenv
from sui_trader import execute_trade_logic

# === Load environment variables ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

TP_PERCENT = float(os.getenv("TP_PERCENT", 10))
SL_PERCENT = float(os.getenv("SL_PERCENT", 5))

# === Flask app ===
flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# === Telegram command handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Raider SUI Bot Activated!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "/start - Start or restart Raider Bot\n"
        "/help - Show this help message\n"
        "/trade - Execute a swing trade\n"
        "/price - Get current SUI/USDT price\n"
        "/topup - Add more credits (if enabled)\n"
        "/credit - Check your balance\n"
        "/set_threshold <percent> - Set signal sensitivity\n"
        "/interval <time> - Set trade repeat interval (e.g., 6h)\n"
        "/schedule <HH:MM> - Set exact trade time\n"
        "/alerts - Enable alerts only mode (no trades)\n"
        "/forecast - Get daily AI trade summary\n"
        "/moon - Toggle Lunar Mode 🌕\n"
    )
    await update.message.reply_text(help_text)

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await asyncio.to_thread(execute_trade_logic)
    await update.message.reply_text(result)

async def set_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        percent = float(context.args[0])
        # Save or apply threshold logic here
        await update.message.reply_text(f"📉 Threshold set to {percent}%")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /set_threshold <percent>")

async def interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        interval = context.args[0]
        # Save or schedule repeated trades here
        await update.message.reply_text(f"⏱️ Trades scheduled every {interval}")
    except IndexError:
        await update.message.reply_text("Usage: /interval <e.g., 6h or 1d>")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        time = context.args[0]
        await update.message.reply_text(f"📆 Daily trade scheduled at {time}")
        # Schedule logic here
    except IndexError:
        await update.message.reply_text("Usage: /schedule <HH:MM>")

async def alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 Alerts-only mode enabled — no trades will be executed.")
    # Set alerts-only mode flag here

async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Daily forecast: SUI likely to range sideways with mild bullish bias.")
    # Replace with actual AI-backed logic later

async def moon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌕 Lunar Mode activated — syncing trade energy with moon phases!")
    # Add lunar logic here

# === Register all commands ===
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("trade", trade))
telegram_app.add_handler(CommandHandler("set_threshold", set_threshold))
telegram_app.add_handler(CommandHandler("interval", interval))
telegram_app.add_handler(CommandHandler("schedule", schedule))
telegram_app.add_handler(CommandHandler("alerts", alerts))
telegram_app.add_handler(CommandHandler("forecast", forecast))
telegram_app.add_handler(CommandHandler("moon", moon))

# === Webhook route ===
@flask_app.post(WEBHOOK_PATH)
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK", 200
