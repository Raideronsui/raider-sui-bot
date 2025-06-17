HEAD
from flask import Flask, request
from telegram import Update
import os
import logging
8afa747 (Temp: Save local changes before rebase)
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Example command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello from webhook!")

telegram_app.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

@app.before_first_request
def set_webhook():
    telegram_app.bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
