import os
import asyncio
import threading

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

# ---------------- FLASK ----------------

web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Medical Radar Bot Running"

# ---------------- TELEGRAM ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo 🚀")

async def run_telegram():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("BOT START")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("RUNNING")

    while True:
        await asyncio.sleep(60)

def start_bot():
    asyncio.run(run_telegram())

# ---------------- MAIN ----------------

if __name__ == "__main__":

    threading.Thread(target=start_bot).start()

    port = int(os.environ.get("PORT", 10000))

    web_app.run(
        host="0.0.0.0",
        port=port
    )
