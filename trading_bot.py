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
from config import (
    set_threshold, get_threshold,
    set_alert_mode, is_alerts_only,
    set_moon_mode, is_moon_mode
)

# === Load environment variables ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

# === Flask app ===
flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# === Telegram commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Raider SUI Bot Activated!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "/start - Start or restart Raider Bot\n"
        "/help - Show this help message\n"
        "/trade - Execute a swing trade\n"
        "/price - Get current SUI/USDT price\n"
        "/set_threshold <percent> - Set trigger threshold\n"
        "/alerts_on or /alerts_off - Enable or disable alerts-only mode\n"
        "/moon_on or /moon_off - Toggle lunar mode\n"
        "/credit - Check your balance"
    )
    await update.message.reply_text(help_text)

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await asyncio.to_thread(execute_trade_logic)
    await update.message.reply_text(result)

async def set_threshold_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])
        set_threshold(update.effective_user.id, value)
        await update.message.reply_text(f"📊 Threshold set to {value}%")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /set_threshold <percent>")

async def alerts_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_alert_mode(update.effective_user.id, True)
    await update.message.reply_text("🔔 Alerts-only mode enabled.")

async def alerts_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_alert_mode(update.effective_user.id, False)
    await update.message.reply_text("🔕 Alerts-only mode disabled.")

async def moon_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_moon_mode(update.effective_user.id, True)
    await update.message.reply_text("🌕 Lunar mode enabled.")

async def moon_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_moon_mode(update.effective_user.id, False)
    await update.message.reply_text("🌑 Lunar mode disabled.")

# === Add handlers ===
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("trade", trade))
telegram_app.add_handler(CommandHandler("set_threshold", set_threshold_cmd))
telegram_app.add_handler(CommandHandler("alerts_on", alerts_on))
telegram_app.add_handler(CommandHandler("alerts_off", alerts_off))
telegram_app.add_handler(CommandHandler("moon_on", moon_on))
telegram_app.add_handler(CommandHandler("moon_off", moon_off))

# === Webhook route ===
@flask_app.post(WEBHOOK_PATH)
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK", 200

# === Entrypoint ===
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

