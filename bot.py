from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from radar import scan_jobs
from config import TOKEN

from flask import Flask
import threading

# -------------------------
# MINI WEB SERVER (RENDER FIX)
# -------------------------
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot activo"


def run_web():
    web_app.run(host="0.0.0.0", port=10000)


# -------------------------
# TELEGRAM BOT
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await update.message.reply_text(
        f"🧠 Medical Radar activo.\nCHAT ID: {chat_id}"
    )


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Escaneando hospitales...")

    jobs = scan_jobs()

    if not jobs:
        await update.message.reply_text("No se encontraron resultados.")
        return

    for job in jobs:
        await update.message.reply_text(job)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", scan))


# -------------------------
# START BOTH SYSTEMS
# -------------------------
if __name__ == "__main__":
    print("Bot iniciando...")

    # Web server para Render
    threading.Thread(target=run_web).start()

    # Telegram bot
    app.run_polling()
