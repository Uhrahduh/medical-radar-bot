from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from radar import scan_jobs
from config import TOKEN

from flask import Flask
import threading
from apscheduler.schedulers.background import BackgroundScheduler

# ------------------------
# FLASK (RENDER FIX)
# ------------------------
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Medical Radar activo"


def run_web():
    web_app.run(host="0.0.0.0", port=10000)


# ------------------------
# TELEGRAM BOT
# ------------------------
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


# ------------------------
# AUTOMATIC SCANNER
# ------------------------
def auto_scan(app_bot):
    jobs = scan_jobs()

    for job in jobs:
        app_bot.bot.send_message(chat_id=app_bot.chat_id, text=job)


# ------------------------
# MAIN
# ------------------------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("scan", scan))


def start_scheduler(app_bot):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: auto_scan(app_bot), "interval", minutes=5)
    scheduler.start()


if __name__ == "__main__":
    print("Bot iniciando...")

    threading.Thread(target=run_web).start()

    start_scheduler(app)

    app.run_polling()
