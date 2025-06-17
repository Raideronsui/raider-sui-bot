import os
import asyncio
import datetime
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from dotenv import load_dotenv
from sui_trader import execute_trade_logic, get_current_price  # Make sure these are implemented

# === Load environment variables ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

# === Global Config State ===
CONFIG = {
    "alerts_only": False,
    "trade_threshold": 5.0,
    "interval_hours": None,
    "scheduled_time": None,
    "lunar_mode": False
}

# === Flask app ===
flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# === Telegram Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Raider SUI Bot Activated!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🧠 Raider SUI Bot Commands:\n"
        "/start - Start or restart the bot\n"
        "/help - Show this help message\n"
        "/trade - Execute a swing trade now\n"
        "/price - Get current SUI/USDT price\n"
        "/interval 6h - Set auto trade every X hours\n"
        "/schedule 09:00 - Set trade time daily\n"
        "/set_threshold 5 - Set % threshold for signals\n"
        "/alerts_only on/off - Just alerts, no trading\n"
        "/forecast - AI-backed daily forecast (WIP)\n"
        "/lunar_mode on/off - Enable moon phase mode 🌕\n"
        "/chart - Show current SUI chart (WIP)"
    )
    await update.message.reply_text(help_text)

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if CONFIG["alerts_only"]:
        await update.message.reply_text("🔔 Signal detected, but alerts-only mode is ON.")
        return
    result = await asyncio.to_thread(execute_trade_logic)
    await update.message.reply_text(result)

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_current_price()
    await update.message.reply_text(f"💱 Current SUI/USDT: {price}")

async def set_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        threshold = float(context.args[0])
        CONFIG["trade_threshold"] = threshold
        await update.message.reply_text(f"📉 Trade threshold set to {threshold}%")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Usage: /set_threshold 5")

async def interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        hours = int(context.args[0].replace("h", ""))
        CONFIG["interval_hours"] = hours
        await update.message.reply_text(f"⏱️ Trades will run every {hours} hours.")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Usage: /interval 6")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        time_str = context.args[0]
        datetime.datetime.strptime(time_str, "%H:%M")
        CONFIG["scheduled_time"] = time_str
        await update.message.reply_text(f"🗓️ Daily trade scheduled at {time_str}")
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Usage: /schedule 09:00")

async def alerts_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mode = context.args[0].lower()
        CONFIG["alerts_only"] = (mode == "on")
        state = "enabled" if CONFIG["alerts_only"] else "disabled"
        await update.message.reply_text(f"🔔 Alerts-only mode {state}.")
    except IndexError:
        await update.message.reply_text("⚠️ Usage: /alerts_only on/off")

async def forecast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 AI forecast feature is coming soon...")

async def lunar_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mode = context.args[0].lower()
        CONFIG["lunar_mode"] = (mode == "on")
        state = "enabled" if CONFIG["lunar_mode"] else "disabled"
        await update.message.reply_text(f"🌕 Lunar mode {state}.")
    except IndexError:
        await update.message.reply_text("⚠️ Usage: /lunar_mode on/off")

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Chart image feature coming soon...")

# === Register Handlers ===
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("trade", trade))
telegram_app.add_handler(CommandHandler("price", price))
telegram_app.add_handler(CommandHandler("interval", interval))
telegram_app.add_handler(CommandHandler("schedule", schedule))
telegram_app.add_handler(CommandHandler("set_threshold", set_threshold))
telegram_app.add_handler(CommandHandler("alerts_only", alerts_only))
telegram_app.add_handler(CommandHandler("forecast", forecast))
telegram_app.add_handler(CommandHandler("lunar_mode", lunar_mode))
telegram_app.add_handler(CommandHandler("chart", chart))

# === Webhook route ===
@flask_app.post(WEBHOOK_PATH)
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK", 200

# === Entrypoint ===
if __name__ == "__main__":
    async def run_bot():
        await telegram_app.bot.delete_webhook(drop_pending_updates=True)
        await telegram_app.bot.set_webhook(WEBHOOK_URL)
        print(f"🌐 Webhook set to: {WEBHOOK_URL}")
    asyncio.run(run_bot())
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
