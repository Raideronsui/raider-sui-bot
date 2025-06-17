import os
from flask import Flask, request
from telegram import Update
from telegram.ext import
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,

from dotenv import load_dotenv
from sui_trader import execute_trade_logic

# === Load .env ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"

# === Flask App ===
flask_app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# === Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Raider SUI Bot Activated!")

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = execute_trade_logic()
    await update.message.reply_text(f"Trade result: {result}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("trade", trade))

# === Webhook Route ===
@flask_app.post(WEBHOOK_PATH)
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK", 200

# === Webhook Setup ===
@flask_app.before_first_request
def init_webhook():
    telegram_app.bot.delete_webhook()
    telegram_app.bot.set_webhook(WEBHOOK_URL)
    print(f"🌐 Webhook set to: {WEBHOOK_URL}")

# === Entrypoint ===
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)
