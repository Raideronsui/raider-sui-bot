import os
import sui_trader
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import ApplicationBuilder, CommandHandler

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def start(update, ctx): await update.message.reply_text("🚀 Raider Swing Bot is online.")
async def trade(update, ctx): await update.message.reply_text(f"🟢 Trade Result:\n{sui_trader.perform_trade()}")
async def status(update, ctx):
    amount_out, fee = sui_trader.fetch_price()
    await update.message.reply_text(f"1 SUI → {amount_out} USDC; est. fee {fee} SUI")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trade", trade))
app.add_handler(CommandHandler("status", status))

def auto_trade():
    res = sui_trader.perform_trade()
    app.bot.send_message(chat_id=CHAT_ID, text=f"⏰ Auto Trade Result:\n{res}")

scheduler = BackgroundScheduler()
scheduler.add_job(auto_trade, 'interval', hours=6)
scheduler.start()

if __name__ == "__main__":
    app.run_polling()
