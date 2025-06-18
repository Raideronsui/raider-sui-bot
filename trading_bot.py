import logging
import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import (
    BOT_TOKEN,
    set_threshold,
    get_threshold_percent,
    set_alert_mode,
    get_alerts_only,
    set_moon_mode,
    get_moon_mode,
)
from sui_trader import execute_trade_logic

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

@app.route("/")
def home():
    return "✅ Raider SUI Bot is live!"

# --- Telegram Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Raider SUI Trading Bot!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Welcome message\n"
        "/help - List commands\n"
        "/price - Show SUI price and trade info\n"
        "/threshold <value> - Set trade threshold %\n"
        "/alertson /alertsoff - Toggle alerts-only mode\n"
        "/moonon /moonoff - Toggle moon mode\n"
        "/credit - View wallet info\n"
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = execute_trade_logic()
    await update.message.reply_text(msg)

async def credit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 Wallet and RPC bound.")

async def threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        value = context.args[0]
        result = set_threshold(value)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text(f"Current threshold: {get_threshold_percent()}%")

async def alertson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(set_alert_mode(True))

async def alertsoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(set_alert_mode(False))

async def moonon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(set_moon_mode(True))

async def moonoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(set_moon_mode(False))

# --- Register Commands ---
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("price", price))
application.add_handler(CommandHandler("credit", credit))
application.add_handler(CommandHandler("threshold", threshold))
application.add_handler(CommandHandler("alertson", alertson))
application.add_handler(CommandHandler("alertsoff", alertsoff))
application.add_handler(CommandHandler("moonon", moonon))
application.add_handler(CommandHandler("moonoff", moonoff))

if __name__ == "__main__":
    import threading
    threading.Thread(target=application.run_polling).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
